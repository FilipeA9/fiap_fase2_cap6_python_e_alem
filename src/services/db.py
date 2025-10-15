"""Camada de persistência Oracle com fallback informativo."""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any, Dict, Iterable, List, Optional

from .arquivos import registrar_log

try:  # pragma: no cover - importação depende do ambiente Oracle
    import oracledb
except Exception:  # pragma: no cover - fallback
    oracledb = None  # type: ignore


class OracleIndisponivel(RuntimeError):
    """Exceção lançada quando não é possível estabelecer conexão com Oracle."""


@contextmanager
def obter_conexao() -> Iterable[Any]:
    """Obtém conexão Oracle utilizando variáveis de ambiente."""

    if oracledb is None:
        raise OracleIndisponivel("Driver Oracle não disponível no ambiente atual.")
    usuario = os.getenv("DB_USER")
    senha = os.getenv("DB_PASS")
    dsn = os.getenv("DB_DSN")
    if not all([usuario, senha, dsn]):
        raise OracleIndisponivel("Variáveis de ambiente do banco não configuradas.")
    conn = oracledb.connect(user=usuario, password=senha, dsn=dsn)
    try:
        yield conn
    finally:
        conn.close()


def inserir_preco_oracle(conn, registro: Dict) -> None:
    """Insere registro de preço na tabela ``PRICES``."""

    sql = (
        "INSERT INTO PRICES (data_ref, product_id, market_id, tipo_preco, unidade_orig, "
        "preco_orig, preco_kg, fonte) "
        "VALUES (:data_ref, :product_id, :market_id, :tipo_preco, :unidade_orig, :preco_orig, :preco_kg, :fonte)"
    )
    cursor = conn.cursor()
    try:
        cursor.execute(
            sql,
            {
                "data_ref": registro["data_ref"],
                "product_id": registro["product_id"],
                "market_id": registro["market_id"],
                "tipo_preco": registro["tipo_preco"],
                "unidade_orig": registro.get("unidade_original"),
                "preco_orig": registro["preco_original"],
                "preco_kg": registro["preco_kg"],
                "fonte": registro["fonte"],
            },
        )
        conn.commit()
        registrar_log("INSERT_ORACLE", "SUCESSO", f"Registro inserido em PRICES ({registro['data_ref']})")
    finally:
        cursor.close()


def consultar_oracle(conn, filtros: Dict) -> List[Dict[str, Any]]:
    """Consulta registros em ``PRICES`` com filtros opcionais."""

    sql = [
        "SELECT pr.data_ref, p.codigo, m.nome as mercado, pr.tipo_preco, pr.preco_kg,",
        "       pr.preco_orig, pr.unidade_orig, pr.fonte",
        "  FROM PRICES pr",
        "  JOIN PRODUCTS p ON p.product_id = pr.product_id",
        "  JOIN MARKETS  m ON m.market_id = pr.market_id",
        " WHERE 1=1",
    ]
    params: Dict[str, Any] = {}

    if filtros.get("produto"):
        sql.append("   AND p.codigo = :produto")
        params["produto"] = filtros["produto"]
    if filtros.get("mercado"):
        sql.append("   AND m.nome = :mercado")
        params["mercado"] = filtros["mercado"]
    if filtros.get("tipo_preco"):
        sql.append("   AND pr.tipo_preco = :tipo_preco")
        params["tipo_preco"] = filtros["tipo_preco"]
    if filtros.get("data_inicial"):
        sql.append("   AND pr.data_ref >= :data_inicial")
        params["data_inicial"] = filtros["data_inicial"]
    if filtros.get("data_final"):
        sql.append("   AND pr.data_ref <= :data_final")
        params["data_final"] = filtros["data_final"]
    sql.append(" ORDER BY pr.data_ref")

    cursor = conn.cursor()
    try:
        cursor.execute("\n".join(sql), params)
        colunas = [d[0].lower() for d in cursor.description]
        registros = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]
        registrar_log("CONSULTA_ORACLE", "SUCESSO", f"{len(registros)} registro(s) retornados")
        return registros
    finally:
        cursor.close()


def inserir_produto_oracle(conn, codigo: str, nome: str, categoria: Optional[str]) -> None:
    """Insere produto em ``PRODUCTS`` se ainda não existir."""

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT product_id FROM PRODUCTS WHERE codigo = :codigo", {"codigo": codigo})
        if cursor.fetchone():
            return
        cursor.execute(
            "INSERT INTO PRODUCTS (codigo, nome, categoria) VALUES (:codigo, :nome, :categoria)",
            {"codigo": codigo, "nome": nome, "categoria": categoria},
        )
        conn.commit()
        registrar_log("INSERT_PRODUTO", "SUCESSO", codigo)
    finally:
        cursor.close()


def inserir_mercado_oracle(conn, nome: str, tipo: str) -> None:
    """Insere mercado em ``MARKETS`` se ainda não existir."""

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT market_id FROM MARKETS WHERE nome = :nome", {"nome": nome})
        if cursor.fetchone():
            return
        cursor.execute(
            "INSERT INTO MARKETS (nome, tipo) VALUES (:nome, :tipo)",
            {"nome": nome, "tipo": tipo},
        )
        conn.commit()
        registrar_log("INSERT_MERCADO", "SUCESSO", nome)
    finally:
        cursor.close()


def obter_ids(conn, produto: str, mercado: str) -> tuple[int, int]:
    """Obtém identificadores internos de produto e mercado."""

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT product_id FROM PRODUCTS WHERE codigo = :codigo", {"codigo": produto})
        produto_row = cursor.fetchone()
        if not produto_row:
            raise ValueError("Produto não encontrado no Oracle.")
        cursor.execute("SELECT market_id FROM MARKETS WHERE nome = :nome", {"nome": mercado})
        mercado_row = cursor.fetchone()
        if not mercado_row:
            raise ValueError("Mercado não encontrado no Oracle.")
        return int(produto_row[0]), int(mercado_row[0])
    finally:
        cursor.close()
