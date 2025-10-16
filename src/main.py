"""Interface de linha de comando do Monitor de Preços Agro."""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from tabulate import tabulate

from src.config.params import carregar_parametros
from src.models.entidades import RegistroPreco
from src.services import arquivos, db, regras, validacao

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def carregar_dados_iniciais() -> tuple[Dict, Dict, List[dict]]:
    """Carrega produtos, mercados e observações pendentes."""

    produtos = arquivos.carregar_json(DATA_DIR / "produtos.json", {})
    mercados = arquivos.carregar_json(DATA_DIR / "mercados.json", {})
    observacoes = arquivos.carregar_json(DATA_DIR / "observacoes.json", [])
    return produtos, mercados, observacoes


def sincronizar_pendentes(conexao, observacoes: List[dict]) -> None:
    """Sincroniza mercados, produtos e observações locais com o banco Oracle."""

    # Carrega dados locais
    produtos = arquivos.carregar_json(DATA_DIR / "produtos.json", {})
    mercados = arquivos.carregar_json(DATA_DIR / "mercados.json", {})
    observacoes = arquivos.carregar_json(DATA_DIR / "observacoes.json", [])

    # Sincroniza mercados
    for nome, dados in mercados.items():
        try:
            db.inserir_mercado_oracle(conexao, nome, dados.get("tipo", ""))
        except Exception as exc:
            arquivos.registrar_log("SYNC_MERCADO", "ERRO", f"{nome}: {exc}", nivel="WARN")

    # Sincroniza produtos
    for codigo, dados in produtos.items():
        try:
            db.inserir_produto_oracle(conexao, codigo, dados.get("nome", ""), dados.get("categoria", ""))
        except Exception as exc:
            arquivos.registrar_log("SYNC_PRODUTO", "ERRO", f"{codigo}: {exc}", nivel="WARN")

    # Sincroniza observações (registros de preço)
    for obs in observacoes:
        try:
            produto_id, mercado_id = db.obter_ids(conexao, obs["produto"], obs["mercado"])
            registro = {
                "data_ref": obs["data_ref"],
                "product_id": produto_id,
                "market_id": mercado_id,
                "tipo_preco": obs["tipo_preco"],
                "unidade_original": obs["unidade_original"],
                "preco_original": obs["preco_original"],
                "preco_kg": obs["preco_kg"],
                "fonte": obs["fonte"],
            }
            db.inserir_preco_oracle(conexao, registro)
        except Exception as exc:
            arquivos.registrar_log("SYNC_PRECO", "ERRO", f"{obs.get('produto', '')}: {exc}", nivel="WARN")

    # Limpa arquivos locais após sincronização
    arquivos.salvar_json(DATA_DIR / "produtos.json", {})
    arquivos.salvar_json(DATA_DIR / "mercados.json", {})
    arquivos.salvar_json(DATA_DIR / "observacoes.json", [])

    arquivos.registrar_log("SYNC_FINALIZADA", "SUCESSO", "Pendentes sincronizados e arquivos limpos.")


def registrar_preco(
    produtos: Dict,
    mercados: Dict,
    fatores: Dict,
    historico: List[dict],
    observacoes: List[dict],
    conexao,
) -> None:
    """Fluxo de registro de preço."""

    print("\n-- Registrar preço --")
    dados = {
        "data_ref": input("Data (YYYY-MM-DD): ").strip(),
        "produto": input("Produto (código): ").strip(),
        "mercado": input("Mercado (nome): ").strip(),
        "tipo_preco": input("Tipo de preço [ATACADO_MIN/ATACADO_MED/ATACADO_MAX/VAREJO]: ").strip(),
        "unidade_original": input("Unidade original (ex.: kg, cx23kg): ").strip(),
        "preco_original": input("Preço original: ").strip(),
        "fonte": input("Fonte (CEASA, Coleta manual...): ").strip(),
    }

    existentes = {
        (
            r["data_ref"].strftime("%Y-%m-%d"),
            r["produto"],
            r["mercado"],
            r["tipo_preco"],
        )
        for r in historico
    }
    dados["registros_existentes"] = existentes

    try:
        validacao.validar_registro(dados, produtos, mercados, fatores, conexao)
    except ValueError as exc:
        print(f"Erro de validação: {exc}")
        arquivos.registrar_log("REGISTRAR_PRECO", "ERRO", str(exc))
        return

    preco_original = float(dados["preco_original"])
    preco_kg = regras.normalizar_unidade(preco_original, dados["unidade_original"], fatores)
    data_ref = datetime.strptime(dados["data_ref"], "%Y-%m-%d").date()

    registro_local = RegistroPreco(
        data_ref=data_ref,
        produto=dados["produto"],
        mercado=dados["mercado"],
        tipo_preco=dados["tipo_preco"],
        unidade_original=dados["unidade_original"],
        preco_original=preco_original,
        preco_kg=preco_kg,
        fonte=dados["fonte"],
    )
    sucesso_oracle = False

    if conexao is not None:
        try:  # pragma: no cover - depende de Oracle
            produto_id, mercado_id = db.obter_ids(conexao, registro_local.produto, registro_local.mercado)
            db.inserir_preco_oracle(
                conexao,
                {
                    "data_ref": registro_local.data_ref,
                    "product_id": produto_id,
                    "market_id": mercado_id,
                    "tipo_preco": registro_local.tipo_preco,
                    "unidade_original": registro_local.unidade_original,
                    "preco_original": registro_local.preco_original,
                    "preco_kg": registro_local.preco_kg,
                    "fonte": registro_local.fonte,
                },
            )
            sucesso_oracle = True
        except Exception as exc:  # pragma: no cover - depende do ambiente Oracle
            arquivos.registrar_log("REGISTRAR_PRECO", "ERRO", str(exc), nivel="WARN")
            print("Oracle indisponível. Registro salvo em contingência JSON.")

    registro_dict = registro_local.__dict__.copy()
    registro_dict["pendente_sync"] = not sucesso_oracle
    historico.append({**registro_dict})
    if not sucesso_oracle:
        observacoes.append({**registro_dict, "data_ref": registro_local.data_ref.strftime("%Y-%m-%d")})
        arquivos.salvar_json(DATA_DIR / "observacoes.json", observacoes)

    arquivos.registrar_log("REGISTRAR_PRECO", "SUCESSO", f"{registro_local.produto} {registro_local.data_ref}")

    serie = regras.construir_serie(historico, registro_local.produto, registro_local.mercado, registro_local.tipo_preco)
    media7 = regras.media_movel(serie)
    desvio = regras.desvio_padrao(serie)
    variacao = None
    if len(serie) >= 2:
        variacao = regras.variacao_percentual(serie[-1], serie[-2])
    alerta = regras.detectar_alerta(serie[-1], serie)

    print("\nResumo do registro:")
    print(f"Preço normalizado (kg): R$ {registro_local.preco_kg:.2f}")
    print(f"Média móvel (7d): {media7:.2f}" if media7 is not None else "Média móvel (7d): —")
    print(f"Desvio padrão: {desvio:.2f}" if desvio is not None else "Desvio padrão: —")
    if variacao is not None:
        print(f"Variação diária: {variacao:.2f}%")
    else:
        print("Variação diária: —")
    if alerta:
        print(f"ALERTA: {alerta['tipo']} - {alerta['detalhes']}")


def cadastrar_produto(produtos: Dict, conexao) -> None:
    """Fluxo de cadastro de produto."""

    print("\n-- Cadastrar produto --")
    codigo = input("Código (ex.: TOM_LV): ").strip()
    if not codigo:
        print("Código é obrigatório.")
        return
    if codigo in produtos:
        print("Produto já cadastrado.")
        return
    nome = input("Nome: ").strip()
    categoria = input("Categoria: ").strip() or None
    produtos[codigo] = {"nome": nome, "categoria": categoria}
    arquivos.salvar_json(DATA_DIR / "produtos.json", produtos)
    arquivos.registrar_log("CAD_PRODUTO", "SUCESSO", codigo)

    if conexao is not None:
        try:  # pragma: no cover - depende de Oracle
            db.inserir_produto_oracle(conexao, codigo, nome, categoria)
        except Exception as exc:
            arquivos.registrar_log("CAD_PRODUTO", "ERRO", str(exc), nivel="WARN")
            print("Aviso: não foi possível sincronizar com Oracle agora.")


def cadastrar_mercado(mercados: Dict, conexao) -> None:
    """Fluxo de cadastro de mercado."""

    print("\n-- Cadastrar mercado --")
    nome = input("Nome (ex.: CEASA-GO): ").strip()
    if not nome:
        print("Nome é obrigatório.")
        return
    if nome in mercados:
        print("Mercado já cadastrado.")
        return
    tipo = input("Tipo [ATACADO/VAREJO]: ").strip().upper()
    if tipo not in {"ATACADO", "VAREJO"}:
        print("Tipo inválido.")
        return
    mercados[nome] = {"tipo": tipo}
    arquivos.salvar_json(DATA_DIR / "mercados.json", mercados)
    arquivos.registrar_log("CAD_MERCADO", "SUCESSO", nome)

    if conexao is not None:
        try:  # pragma: no cover - depende de Oracle
            db.inserir_mercado_oracle(conexao, nome, tipo)
        except Exception as exc:
            arquivos.registrar_log("CAD_MERCADO", "ERRO", str(exc), nivel="WARN")
            print("Aviso: não foi possível sincronizar com Oracle agora.")


def consultar_historico(historico: List[dict], filtros: Optional[Dict] = None, conexao=None) -> List[dict]:
    """Consulta registros no Oracle se houver conexão, senão filtra localmente."""

    filtros = filtros or {}
    if conexao is not None:
        try:
            registros = db.consultar_oracle(conexao, filtros)
            # Ajusta datas para datetime.date e mantém compatibilidade com o restante do código
            for registro in registros:
                if isinstance(registro["data_ref"], str):
                    registro["data_ref"] = datetime.strptime(registro["data_ref"], "%Y-%m-%d").date()
            return registros
        except Exception as exc:
            arquivos.registrar_log("CONSULTA_ORACLE", "ERRO", str(exc), nivel="WARN")
            print("Erro ao consultar Oracle. Exibindo registros locais.")
    # Consulta local
    registros = []
    for registro in historico:
        if filtros.get("produto") and registro["produto"] != filtros["produto"]:
            continue
        if filtros.get("mercado") and registro["mercado"] != filtros["mercado"]:
            continue
        if filtros.get("tipo_preco") and registro["tipo_preco"] != filtros["tipo_preco"]:
            continue
        if filtros.get("data_inicial") and registro["data_ref"] < filtros["data_inicial"]:
            continue
        if filtros.get("data_final") and registro["data_ref"] > filtros["data_final"]:
            continue
        registros.append(registro)
    return registros


def exibir_consulta(historico: List[dict]) -> tuple[List[dict], List[str]]:
    """Calcula métricas e exibe tabela formatada."""

    linhas = []
    alertas = []
    for registro in sorted(historico, key=lambda r: r["data_ref"]):
        serie = regras.construir_serie(historico, registro["produto"], registro["mercado"], registro["tipo_preco"])
        media7 = regras.media_movel(serie)
        desvio = regras.desvio_padrao(serie)
        variacao = None
        if len(serie) >= 2:
            variacao = regras.variacao_percentual(serie[-1], serie[-2])
        alerta = regras.detectar_alerta(serie[-1], serie)
        if alerta:
            alertas.append(
                f"{registro['data_ref']:%Y-%m-%d} {registro['produto']} {registro['mercado']} {alerta['tipo']}"
            )
        linhas.append(
            {
                "Data": registro["data_ref"].strftime("%Y-%m-%d"),
                "Produto": registro["produto"],
                "Mercado": registro["mercado"],
                "Tipo": registro["tipo_preco"],
                "Preco/kg": f"R$ {registro['preco_kg']:.2f}",
                "Media7": f"{media7:.2f}" if media7 is not None else "—",
                "Var%": f"{variacao:.2f}%" if variacao is not None else "—",
                "Alerta": alerta["tipo"] if alerta else "",
            }
        )
    if linhas:
        print(tabulate(linhas, headers="keys", tablefmt="github"))
    else:
        print("Nenhum registro encontrado.")
    return linhas, alertas


def menu_parametros(parametros) -> None:
    """Exibe parâmetros atuais e orientações de alteração."""

    print("\n-- Parâmetros atuais --")
    print(f"Janela média móvel: {parametros.media_window}")
    print(f"Z-score limite: {parametros.zscore_limite}")
    print(f"Limiar de queda (%): {parametros.limiar_queda}")
    print("Unidades disponíveis:")
    for unidade, fator in parametros.fatores_unidade.items():
        print(f"  - {unidade}: {fator} kg")
    print("\nPara alterar os parâmetros edite config/parametros.json e config/unidades.json e reinicie a aplicação.")


def main() -> None:
    """Função principal que executa o loop do menu."""

    parametros = carregar_parametros()
    regras.atualizar_parametros(parametros.media_window, parametros.zscore_limite, parametros.limiar_queda)

    produtos, mercados, observacoes = carregar_dados_iniciais()
    historico = [
        {
            "data_ref": datetime.strptime(obs["data_ref"], "%Y-%m-%d").date(),
            "produto": obs["produto"],
            "mercado": obs["mercado"],
            "tipo_preco": obs["tipo_preco"],
            "unidade_original": obs["unidade_original"],
            "preco_original": obs["preco_original"],
            "preco_kg": obs["preco_kg"],
            "fonte": obs["fonte"],
            "pendente_sync": obs.get("pendente_sync", False),
        }
        for obs in observacoes
    ]

    conexao = None
    try:
        with db.obter_conexao() as conn:  # pragma: no cover - depende de Oracle
            conexao = conn
            sincronizar_pendentes(conexao, observacoes)
    except Exception as exc:
        arquivos.registrar_log("CONEXAO_ORACLE", "ERRO", str(exc), nivel="WARN")
        conexao = None

    ultima_consulta: List[dict] = []
    ultima_alerta: List[str] = []

    while True:
        print(
            """
1. Cadastrar produto
2. Cadastrar mercado
3. Registrar preço
4. Consultar histórico
5. Exportar resultados
6. Parâmetros
0. Sair
"""
        )
        opcao = input("Selecione uma opção: ").strip()
        if opcao == "1":
            cadastrar_produto(produtos, conexao)
        elif opcao == "2":
            cadastrar_mercado(mercados, conexao)
        elif opcao == "3":
            registrar_preco(produtos, mercados, parametros.fatores_unidade, historico, observacoes, conexao)
        elif opcao == "4":
            filtros = {}
            data_inicial = input("Data inicial (YYYY-MM-DD) ou Enter: ").strip()
            data_final = input("Data final (YYYY-MM-DD) ou Enter: ").strip()
            produto = input("Produto (código) ou Enter: ").strip()
            mercado = input("Mercado (nome) ou Enter: ").strip()
            tipo = input("Tipo de preço ou Enter: ").strip()
            if data_inicial:
                filtros["data_inicial"] = datetime.strptime(data_inicial, "%Y-%m-%d").date()
            if data_final:
                filtros["data_final"] = datetime.strptime(data_final, "%Y-%m-%d").date()
            if produto:
                filtros["produto"] = produto
            if mercado:
                filtros["mercado"] = mercado
            if tipo:
                filtros["tipo_preco"] = tipo
            registros_filtrados = consultar_historico(historico, filtros, conexao)
            ultima_consulta, ultima_alerta = exibir_consulta(registros_filtrados)
        elif opcao == "5":
            if not ultima_consulta:
                print("Realize uma consulta antes de exportar.")
                continue
            arquivos.exportar_resultados(ultima_consulta, ultima_alerta)
            print("Exportação concluída em /exports.")
        elif opcao == "6":
            menu_parametros(parametros)
        elif opcao == "0":
            if conexao:
                db.encerrrar_conexao(conexao)
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário.")
        sys.exit(0)
