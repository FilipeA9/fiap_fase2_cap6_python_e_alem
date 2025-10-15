"""Regras de validação de entradas de dados."""
from __future__ import annotations

from datetime import datetime
from typing import Dict

TIPOS_VALIDOS = {"ATACADO_MIN", "ATACADO_MED", "ATACADO_MAX", "VAREJO"}


def validar_registro(dados: Dict, produtos: Dict, mercados: Dict, fatores: Dict) -> None:
    """Valida informações do registro de preço conforme regras de negócio."""

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

    if dados["produto"] not in produtos:
        raise ValueError("Produto inexistente. Cadastre primeiro.")
    if dados["mercado"] not in mercados:
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
