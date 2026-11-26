from __future__ import annotations

from dataclasses import dataclass
from sqlite3 import Row
from typing import Any


@dataclass(slots=True)
class User:
    id: int
    full_name: str
    address: str
    phone: str
    email: str
    password_hash: str
    role: str
    created_at: str

    @classmethod
    def from_row(cls, row: Row | dict[str, Any]) -> "User":
        return cls(
            id=row["id"],
            full_name=row["full_name"],
            address=row["address"] if "address" in row.keys() else "N/A",
            phone=row["phone"],
            email=row["email"],
            password_hash=row["password_hash"],
            role=row["role"],
            created_at=row["created_at"],
        )
