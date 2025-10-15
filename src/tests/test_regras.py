"""Testes unitários das funções de regras de negócio."""
from __future__ import annotations

import math

from src.services import regras


def test_normalizar_unidade():
    fatores = {"kg": 1, "cx23kg": 23}
    assert math.isclose(regras.normalizar_unidade(230.0, "cx23kg", fatores), 10.0)


def test_media_movel():
    valores = [1, 2, 3, 4, 5, 6, 7]
    assert regras.media_movel(valores, n=3) == 6


def test_desvio_padrao():
    valores = [10, 12, 14, 16]
    desvio = regras.desvio_padrao(valores)
    assert desvio is not None
    assert math.isclose(desvio, 2.58199, rel_tol=1e-5)


def test_variacao_percentual():
    assert math.isclose(regras.variacao_percentual(110, 100), 10.0)


def test_detectar_alerta_outlier_alta():
    serie = [10, 10, 10, 10, 10, 10, 25]
    alerta = regras.detectar_alerta(serie[-1], serie)
    assert alerta is not None
    assert alerta["tipo"] == "OUTLIER_ALTA"


def test_detectar_alerta_queda():
    serie = [10, 10, 10, 10, 10, 10, 9]
    alerta = regras.detectar_alerta(serie[-1], serie)
    assert alerta is not None
    assert alerta["tipo"] in {"QUEDA", "OUTLIER_BAIXA"}
