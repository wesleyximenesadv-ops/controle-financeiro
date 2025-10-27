import sqlite3
from pathlib import Path
from typing import Optional
import pandas as pd
from datetime import date, datetime

DB_PATH = Path(__file__).with_name("finance.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,              -- YYYY-MM-DD
            tipo TEXT NOT NULL,              -- 'Despesa' ou 'Receita'
            categoria TEXT NOT NULL,
            subcategoria TEXT NOT NULL,
            descricao TEXT,
            valor REAL NOT NULL,             -- valor positivo
            conta TEXT,
            tags TEXT,
            user_id TEXT                     -- identificador do usuário (multi-tenant)
        )
        """
    )
    # Migração leve: adicionar coluna user_id se não existir
    cur.execute("PRAGMA table_info(transacoes)")
    cols = [r[1] for r in cur.fetchall()]
    if "user_id" not in cols:
        cur.execute("ALTER TABLE transacoes ADD COLUMN user_id TEXT")
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_transacoes_data ON transacoes(data)
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_transacoes_tipo ON transacoes(tipo)
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_transacoes_categoria ON transacoes(categoria)
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_transacoes_user ON transacoes(user_id)
        """
    )
    cur.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_transacoes_user_data ON transacoes(user_id, data)
        """
    )
    conn.commit()


def _to_iso(d: date) -> str:
    if isinstance(d, str):
        # Expecting already in ISO
        return d
    if isinstance(d, datetime):
        d = d.date()
    return d.isoformat()


def add_transaction(
    conn: sqlite3.Connection,
    data_lanc: date,
    tipo: str,
    categoria: str,
    subcategoria: str,
    descricao: str,
    valor: float,
    conta: str,
    tags: str,
    user_id: str,
) -> int:
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO transacoes (data, tipo, categoria, subcategoria, descricao, valor, conta, tags, user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            _to_iso(data_lanc),
            tipo,
            categoria,
            subcategoria,
            descricao,
            float(valor),
            conta,
            tags,
            user_id,
        ),
    )
    conn.commit()
    return cur.lastrowid


def get_transactions(
    conn: sqlite3.Connection,
    user_id: str,
    tipo: Optional[str] = None,
    categoria: Optional[str] = None,
    subcategoria: Optional[str] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    busca: Optional[str] = None,
) -> pd.DataFrame:
    sql = [
        "SELECT id, data, tipo, categoria, subcategoria, descricao, valor, conta, tags FROM transacoes WHERE 1=1",
        "AND user_id = ?",
    ]
    params = [user_id]

    if tipo:
        sql.append("AND tipo = ?")
        params.append(tipo)
    if categoria:
        sql.append("AND categoria = ?")
        params.append(categoria)
    if subcategoria:
        sql.append("AND subcategoria = ?")
        params.append(subcategoria)
    if data_inicio:
        sql.append("AND date(data) >= date(?)")
        params.append(_to_iso(data_inicio))
    if data_fim:
        sql.append("AND date(data) <= date(?)")
        params.append(_to_iso(data_fim))
    if busca:
        sql.append("AND (descricao LIKE ? OR conta LIKE ? OR tags LIKE ?)")
        like = f"%{busca}%"
        params.extend([like, like, like])

    sql.append("ORDER BY date(data) DESC, id DESC")

    df = pd.read_sql_query(" ".join(sql), conn, params=params)
    if not df.empty:
        df["data"] = pd.to_datetime(df["data"]).dt.date
    return df


def get_monthly_cashflow(conn: sqlite3.Connection, inicio: date, fim: date, user_id: str) -> pd.DataFrame:
    sql = """
        SELECT
            strftime('%Y-%m', date(data)) AS ym,
            SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE -valor END) AS valor
        FROM transacoes
        WHERE user_id = ? AND date(data) BETWEEN date(?) AND date(?)
        GROUP BY ym
        ORDER BY ym
    """
    df = pd.read_sql_query(sql, conn, params=[user_id, _to_iso(inicio), _to_iso(fim)])
    if df.empty:
        return df
    # Converter ym para rótulo Mês/Ano em pt-BR
    def ym_to_label(ym: str) -> str:
        d = datetime.strptime(ym + "-01", "%Y-%m-%d")
        meses = [
            "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
            "Jul", "Ago", "Set", "Out", "Nov", "Dez",
        ]
        return f"{meses[d.month-1]}/{d.year}"

    df["mes"] = df["ym"].apply(ym_to_label)
    return df[["mes", "valor"]]


def get_monthly_breakdown(conn: sqlite3.Connection, inicio: date, fim: date, user_id: str) -> pd.DataFrame:
    """Retorna receitas, despesas e saldo por mês entre [inicio, fim]."""
    sql = """
        SELECT
            strftime('%Y-%m', date(data)) AS ym,
            SUM(CASE WHEN tipo = 'Receita' THEN valor ELSE 0 END) AS receitas,
            SUM(CASE WHEN tipo = 'Despesa' THEN valor ELSE 0 END) AS despesas
        FROM transacoes
        WHERE user_id = ? AND date(data) BETWEEN date(?) AND date(?)
        GROUP BY ym
        ORDER BY ym
    """
    df = pd.read_sql_query(sql, conn, params=[user_id, _to_iso(inicio), _to_iso(fim)])
    if df.empty:
        return df
    def ym_to_label(ym: str) -> str:
        d = datetime.strptime(ym + "-01", "%Y-%m-%d")
        meses = [
            "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
            "Jul", "Ago", "Set", "Out", "Nov", "Dez",
        ]
        return f"{meses[d.month-1]}/{d.year}"
    df["mes"] = df["ym"].apply(ym_to_label)
    df["saldo"] = df["receitas"] - df["despesas"]
    return df[["mes", "ym", "receitas", "despesas", "saldo"]]


def get_sum_by_category_and_type(
    conn: sqlite3.Connection,
    user_id: str,
    inicio: date,
    fim: date,
    tipo: str,
) -> pd.DataFrame:
    """Somatório por categoria para um tipo ('Receita' ou 'Despesa') no período."""
    sql = """
        SELECT categoria, SUM(valor) AS valor
        FROM transacoes
        WHERE user_id = ? AND tipo = ? AND date(data) BETWEEN date(?) AND date(?)
        GROUP BY categoria
        ORDER BY valor DESC
    """
    df = pd.read_sql_query(sql, conn, params=[user_id, tipo, _to_iso(inicio), _to_iso(fim)])
    return df
def get_sum_by_category(conn: sqlite3.Connection, filters: dict) -> pd.DataFrame:
    # Somatório de despesas por categoria com filtros básicos aplicados
    sql = [
        "SELECT categoria, SUM(valor) AS valor FROM transacoes WHERE tipo='Despesa'",
        "AND user_id = ?",
    ]
    params = [filters.get("user_id", "")] 

    cat = filters.get("categoria")
    subcat = filters.get("subcategoria")
    inicio = filters.get("data_inicio")
    fim = filters.get("data_fim")
    busca = filters.get("busca")

    if cat and cat != "Todas":
        sql.append("AND categoria = ?")
        params.append(cat)
    if subcat and subcat != "Todas":
        sql.append("AND subcategoria = ?")
        params.append(subcat)
    if inicio:
        sql.append("AND date(data) >= date(?)")
        params.append(_to_iso(inicio))
    if fim:
        sql.append("AND date(data) <= date(?)")
        params.append(_to_iso(fim))
    if busca:
        sql.append("AND (descricao LIKE ? OR conta LIKE ? OR tags LIKE ?)")
        like = f"%{busca}%"
        params.extend([like, like, like])

    sql.append("GROUP BY categoria ORDER BY valor DESC")

    df = pd.read_sql_query(" ".join(sql), conn, params=params)
    return df
