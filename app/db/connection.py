from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

from app.config import DATA_DIR, DB_PATH


class Database:
    def __init__(self, db_path: str | Path = DB_PATH, schema_path: str | Path | None = None):
        self.db_path = Path(db_path)
        self.schema_path = (
            Path(schema_path)
            if schema_path is not None
            else Path(__file__).resolve().parent / "schema.sql"
        )

    def _connect(self) -> sqlite3.Connection:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        conn = self._connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def init_schema(self) -> None:
        script = self.schema_path.read_text(encoding="utf-8")
        with self.get_connection() as conn:
            conn.executescript(script)
            self._ensure_backward_compatible_schema(conn)

    @staticmethod
    def _column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
        rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
        return any(row["name"] == column for row in rows)

    def _ensure_backward_compatible_schema(self, conn: sqlite3.Connection) -> None:
        # Existing databases from earlier versions may miss these columns.
        if not self._column_exists(conn, "users", "address"):
            conn.execute("ALTER TABLE users ADD COLUMN address TEXT NOT NULL DEFAULT 'N/A'")

        if not self._column_exists(conn, "bookings", "scheduled_date"):
            conn.execute(
                "ALTER TABLE bookings ADD COLUMN scheduled_date TEXT NOT NULL DEFAULT '1970-01-01'"
            )

        if not self._column_exists(conn, "bookings", "scheduled_time"):
            conn.execute(
                "ALTER TABLE bookings ADD COLUMN scheduled_time TEXT NOT NULL DEFAULT '00:00'"
            )

        if not self._column_exists(conn, "bookings", "assigned_driver_id"):
            conn.execute("ALTER TABLE bookings ADD COLUMN assigned_driver_id INTEGER")

    def execute(self, query: str, params: tuple[Any, ...] = ()) -> int:
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.lastrowid

    def execute_non_query(self, query: str, params: tuple[Any, ...] = ()) -> int:
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.rowcount

    def fetch_one(self, query: str, params: tuple[Any, ...] = ()) -> sqlite3.Row | None:
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchone()

    def fetch_all(self, query: str, params: tuple[Any, ...] = ()) -> list[sqlite3.Row]:
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return list(cursor.fetchall())


_db_instance: Database | None = None


def get_db() -> Database:
    global _db_instance
    if _db_instance is None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        _db_instance = Database(DB_PATH)
    return _db_instance
