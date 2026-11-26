from __future__ import annotations

from app.db.connection import Database
from app.models.user import User
from app.utils.constants import ROLE_DRIVER


class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    def create_user(
        self,
        full_name: str,
        address: str,
        phone: str,
        email: str,
        password_hash: str,
        role: str,
    ) -> User:
        user_id = self.db.execute(
            """
            INSERT INTO users (full_name, address, phone, email, password_hash, role)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (full_name, address, phone, email, password_hash, role),
        )
        user = self.find_by_id(user_id)
        if user is None:
            raise RuntimeError("Failed to create user")
        return user

    def find_by_email(self, email: str) -> User | None:
        row = self.db.fetch_one("SELECT * FROM users WHERE email = ?", (email,))
        return User.from_row(row) if row else None

    def find_by_id(self, user_id: int) -> User | None:
        row = self.db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
        return User.from_row(row) if row else None

    def list_users(self) -> list[User]:
        rows = self.db.fetch_all("SELECT * FROM users ORDER BY created_at DESC")
        return [User.from_row(row) for row in rows]

    def list_drivers(self) -> list[User]:
        rows = self.db.fetch_all(
            "SELECT * FROM users WHERE role = ? ORDER BY full_name ASC",
            (ROLE_DRIVER,),
        )
        return [User.from_row(row) for row in rows]
