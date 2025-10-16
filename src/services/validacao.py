"""Regras de validação de entradas de dados."""
from __future__ import annotations

from datetime import datetime
from typing import Dict

TIPOS_VALIDOS = {"ATACADO_MIN", "ATACADO_MED", "ATACADO_MAX", "VAREJO"}


def validar_registro(dados: Dict, produtos: Dict, mercados: Dict, fatores: Dict, conexao=None) -> None:
    """Valida informações do registro de preço conforme regras de negócio, consultando banco primeiro."""
    #print("Validando dados do registro:", dados)
    #print("conexao:", conexao)

    obrigatorios = [
        "data_ref",
        "produto",
        "mercado",
        "tipo_preco",
        "unidade_original",
        "preco_original",
        "fonte",
    ]
    for campo in obrigatorios:
        if not dados.get(campo):
            raise ValueError(f"Campo obrigatório não informado: {campo}")

    try:
        datetime.strptime(dados["data_ref"], "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Data inválida. Utilize o formato YYYY-MM-DD.") from exc

    # Verifica produto e mercado no banco primeiro
    produto_existe = False
    mercado_existe = False
    if conexao is not None:
        try:
            from src.services import db

            # Tenta obter IDs no banco
            db.obter_ids(conexao, dados["produto"], dados["mercado"])
            produto_existe = True
            mercado_existe = True
        except Exception as exc:
            #print("Erro ao consultar banco para validação:", exc)
            raise ValueError(str(exc)) from exc

    # Se não encontrou no banco, verifica nas listas locais
    print("produto_existe:", produto_existe)
    print("mercado_existe:", mercado_existe)
    if not produto_existe and dados["produto"] not in produtos:
        raise ValueError("Produto inexistente. Cadastre primeiro.")
    if not mercado_existe and dados["mercado"] not in mercados:
        raise ValueError("Mercado inexistente. Cadastre primeiro.")
    if dados["tipo_preco"] not in TIPOS_VALIDOS:
        raise ValueError("Tipo de preço inválido.")

    preco = float(dados["preco_original"])
    if preco <= 0:
        raise ValueError("Preço deve ser maior que zero.")
    if dados["unidade_original"] not in fatores:
        unidades = ", ".join(sorted(fatores))
        raise ValueError(f"Unidade desconhecida. Utilize uma das seguintes: {unidades}.")

    existentes = dados.get("registros_existentes", set())
    chave = (
        dados["data_ref"],
        dados["produto"],
        dados["mercado"],
        dados["tipo_preco"],
    )
    if chave in existentes:
        raise ValueError("Já existe registro para esta combinação de data/produto/mercado/tipo.")
