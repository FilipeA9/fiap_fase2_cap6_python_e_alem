"""Regras de negócio e cálculos estatísticos do monitor."""
from __future__ import annotations

from math import sqrt
from statistics import mean
from typing import Iterable, List

MEDIA_JANELA_PADRAO = 7
Z_SCORE_LIMITE_PADRAO = 2.0
LIMIAR_QUEDA_PADRAO = -5.0


class RegrasConfig:
    """Configuração dinâmica utilizada pelas funções de cálculo."""

    media_janela = MEDIA_JANELA_PADRAO
    zscore_limite = Z_SCORE_LIMITE_PADRAO
    limiar_queda = LIMIAR_QUEDA_PADRAO


def atualizar_parametros(janela: int, zscore: float, limiar_queda: float) -> None:
    """Atualiza parâmetros globais utilizados nos cálculos."""

    RegrasConfig.media_janela = janela
    RegrasConfig.zscore_limite = zscore
    RegrasConfig.limiar_queda = limiar_queda


def normalizar_unidade(preco: float, unidade: str, fatores: dict) -> float:
    """Converte o ``preco`` para equivalente em quilograma utilizando ``fatores``."""

    if unidade not in fatores:
        raise ValueError(f"Unidade desconhecida: {unidade}")
    fator = float(fatores[unidade])
    if fator <= 0:
        raise ValueError("Fator de unidade inválido")
    return preco / fator


def media_movel(valores: List[float], n: int = RegrasConfig.media_janela) -> float | None:
    """Calcula a média móvel simples dos últimos ``n`` valores."""

    serie = [v for v in valores if v is not None]
    if not serie:
        return None
    janela = serie[-n:]
    return mean(janela)


def desvio_padrao(valores: List[float]) -> float | None:
    """Calcula o desvio padrão amostral da série fornecida."""

    serie = [v for v in valores if v is not None]
    tamanho = len(serie)
    if tamanho < 2:
        return None
    media_valores = mean(serie)
    variancia = sum((x - media_valores) ** 2 for x in serie) / (tamanho - 1)
    return sqrt(variancia)


def variacao_percentual(hoje: float, ontem: float) -> float | None:
    """Calcula a variação percentual diária."""

    if ontem is None or hoje is None:
        return None
    if ontem == 0:
        return None
    return ((hoje - ontem) / ontem) * 100


def detectar_alerta(preco_hoje: float, serie: List[float]) -> dict | None:
    """Retorna um alerta de outlier ou queda acentuada conforme regras de negócio."""

    if not serie:
        return None
    janela = serie[-RegrasConfig.media_janela :]
    media_atual = media_movel(janela)
    desvio = desvio_padrao(janela)
    alerta: dict | None = None

    if media_atual is not None and desvio is not None and desvio > 0:
        limite_superior = media_atual + RegrasConfig.zscore_limite * desvio
        limite_inferior = media_atual - RegrasConfig.zscore_limite * desvio
        if preco_hoje > limite_superior:
            alerta = {
                "tipo": "OUTLIER_ALTA",
                "detalhes": f"Preço acima do limite ({preco_hoje:.2f} > {limite_superior:.2f})",
            }
        elif preco_hoje < limite_inferior:
            alerta = {
                "tipo": "OUTLIER_BAIXA",
                "detalhes": f"Preço abaixo do limite ({preco_hoje:.2f} < {limite_inferior:.2f})",
            }

    if len(janela) >= 2:
        variacao = variacao_percentual(janela[-1], janela[-2])
        if variacao is not None and variacao <= RegrasConfig.limiar_queda:
            alerta = {
                "tipo": "QUEDA",
                "detalhes": f"Queda de {variacao:.2f}% em relação ao dia anterior",
            }
    return alerta


def construir_serie(registros: Iterable[dict], produto: str, mercado: str, tipo: str) -> List[float]:
    """Extrai série histórica para o tripé ``produto``/``mercado``/``tipo``."""

    serie: List[float] = []
    for registro in sorted(registros, key=lambda r: r["data_ref"]):
        if (
            registro.get("produto") == produto
            and registro.get("mercado") == mercado
            and registro.get("tipo_preco") == tipo
        ):
            serie.append(float(registro["preco_kg"]))
    return serie
