"""Entidades do domínio do monitor de preços agro."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(slots=True)
class Produto:
    """Representa um produto hortifrúti monitorado."""

    codigo: str
    nome: str
    categoria: Optional[str] = None


@dataclass(slots=True)
class Mercado:
    """Representa um mercado de referência (atacado ou varejo)."""

    identificador: str
    tipo: str


@dataclass
class RegistroPreco:
    """Registro de preço normalizado utilizado para cálculos e persistência."""

    data_ref: date
    produto: str
    mercado: str
    tipo_preco: str
    unidade_original: str
    preco_original: float
    preco_kg: float
    fonte: str
    pendente_sync: bool = False
