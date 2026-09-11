"""PostgreSQL persistence helpers for application-level agent history.

Qdrant remains responsible for vector search. PostgreSQL stores application
metadata such as agent requests and responses.
"""
from __future__ import annotations

import os
from typing import Any

import psycopg
from psycopg.rows import dict_row


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS agent_runs (
    id BIGSERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    answer TEXT,
    verification_status TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""


def get_database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError("DATABASE_URL is not configured.")
    return url


def get_connection():
    return psycopg.connect(get_database_url(), row_factory=dict_row)


def initialize_database() -> None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TABLE_SQL)
        connection.commit()


def save_agent_run(
    query: str,
    answer: str | None,
    verification_status: str | None = None,
) -> int:
    sql = """
    INSERT INTO agent_runs (query, answer, verification_status)
    VALUES (%s, %s, %s)
    RETURNING id;
    """
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, (query, answer, verification_status))
            row = cursor.fetchone()
        connection.commit()
    return int(row["id"])


def list_agent_runs(limit: int = 20) -> list[dict[str, Any]]:
    limit = max(1, min(limit, 100))
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, query, answer, verification_status, created_at
                FROM agent_runs
                ORDER BY created_at DESC
                LIMIT %s;
                """,
                (limit,),
            )
            return list(cursor.fetchall())


def database_is_available() -> bool:
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                cursor.fetchone()
        return True
    except Exception:
        return False
