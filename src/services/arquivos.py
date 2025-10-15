"""Serviços utilitários para manipulação de arquivos e logs."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
EXPORT_DIR = BASE_DIR / "exports"
LOG_FILE = BASE_DIR / "logs" / "operacoes.txt"


def carregar_json(caminho: Path, padrao: Any) -> Any:
    """Carrega conteúdo JSON retornando ``padrao`` quando inexistente."""

    if not caminho.exists():
        return padrao
    with caminho.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_json(caminho: Path, dados: Any) -> None:
    """Persiste dados em formato JSON com identação."""

    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def registrar_log(acao: str, status: str, detalhes: str, nivel: str = "INFO") -> None:
    """Registra eventos operacionais em ``logs/operacoes.txt``."""

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    momento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"{momento} | {nivel.upper():5} | {acao:20} | {status:7} | {detalhes}\n"
    with LOG_FILE.open("a", encoding="utf-8") as arquivo:
        arquivo.write(linha)


def exportar_resultados(registros: Iterable[dict[str, Any]], alertas: list[str]) -> tuple[Path, Path]:
    """Exporta registros para JSON e relatório texto retornando os caminhos criados."""

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    json_path = EXPORT_DIR / f"consulta-{timestamp}.json"
    txt_path = EXPORT_DIR / f"relatorio-{timestamp}.txt"

    registros_lista = list(registros)
    salvar_json(json_path, registros_lista)

    with txt_path.open("w", encoding="utf-8") as relatorio:
        relatorio.write("Relatório de Consulta de Preços\n")
        relatorio.write(f"Gerado em: {datetime.now():%Y-%m-%d %H:%M}\n\n")
        relatorio.write("Resumo de alertas:\n")
        if alertas:
            for alerta in alertas:
                relatorio.write(f"- {alerta}\n")
        else:
            relatorio.write("- Nenhum alerta no período.\n")
        relatorio.write("\nTotal de registros: {}\n".format(len(registros_lista)))
    registrar_log("EXPORTACAO", "SUCESSO", f"{json_path.name}, {txt_path.name}")
    return json_path, txt_path
