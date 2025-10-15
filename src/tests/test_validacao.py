"""Testes para regras de validação de registros."""
from __future__ import annotations

import pytest

from src.services import validacao


@pytest.fixture
def contexto():
    produtos = {"TOM_LV": {"nome": "Tomate Longa Vida"}}
    mercados = {"CEASA-GO": {"tipo": "ATACADO"}}
    fatores = {"kg": 1, "cx23kg": 23}
    existentes = {("2024-01-01", "TOM_LV", "CEASA-GO", "ATACADO_MED")}
    return produtos, mercados, fatores, existentes


def registro_valido():
    return {
        "data_ref": "2024-01-02",
        "produto": "TOM_LV",
        "mercado": "CEASA-GO",
        "tipo_preco": "ATACADO_MED",
        "unidade_original": "cx23kg",
        "preco_original": 230.0,
        "fonte": "CEASA",
    }


def test_validacao_sucesso(contexto):
    produtos, mercados, fatores, _ = contexto
    dados = registro_valido()
    validacao.validar_registro(dados, produtos, mercados, fatores)


def test_validacao_preco_invalido(contexto):
    produtos, mercados, fatores, _ = contexto
    dados = registro_valido()
    dados["preco_original"] = 0
    with pytest.raises(ValueError):
        validacao.validar_registro(dados, produtos, mercados, fatores)


def test_validacao_unidade_invalida(contexto):
    produtos, mercados, fatores, _ = contexto
    dados = registro_valido()
    dados["unidade_original"] = "saco"
    with pytest.raises(ValueError):
        validacao.validar_registro(dados, produtos, mercados, fatores)


def test_validacao_tipo_invalido(contexto):
    produtos, mercados, fatores, _ = contexto
    dados = registro_valido()
    dados["tipo_preco"] = "MINIMO"
    with pytest.raises(ValueError):
        validacao.validar_registro(dados, produtos, mercados, fatores)


def test_validacao_deduplicacao(contexto):
    produtos, mercados, fatores, existentes = contexto
    dados = registro_valido()
    dados["data_ref"] = "2024-01-01"
    dados["registros_existentes"] = existentes
    with pytest.raises(ValueError):
        validacao.validar_registro(dados, produtos, mercados, fatores)
