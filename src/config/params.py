"""Carregamento de parâmetros de configuração da aplicação."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"


def _ler_json_parametros(caminho: Path) -> Dict[str, Any]:
    import json

    if not caminho.exists():
        return {}
    with caminho.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def _carregar_variaveis_ambiente() -> None:
    load_dotenv(CONFIG_DIR / ".env")


@dataclass(slots=True)
class Parametros:
    """Parâmetros dinâmicos de negócio utilizados nos cálculos."""

    media_window: int = 7
    zscore_limite: float = 2.0
    limiar_queda: float = -5.0
    fatores_unidade: Dict[str, float] | None = None


def carregar_parametros() -> Parametros:
    """Carrega os parâmetros a partir de JSON e variáveis de ambiente."""

    _carregar_variaveis_ambiente()
    parametros = Parametros()

    config_path = CONFIG_DIR / "parametros.json"
    dados_config = _ler_json_parametros(config_path)
    unidades_path = CONFIG_DIR / "unidades.json"
    fatores = _ler_json_parametros(unidades_path)

    parametros.media_window = int(dados_config.get("media_window", parametros.media_window))
    parametros.zscore_limite = float(dados_config.get("zscore_limite", parametros.zscore_limite))
    parametros.limiar_queda = float(dados_config.get("limiar_queda", parametros.limiar_queda))
    parametros.fatores_unidade = {k: float(v) for k, v in fatores.items()} if fatores else {}
    return parametros
