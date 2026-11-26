from __future__ import annotations

import hashlib
import os

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.validation_service import ValidationService
from app.utils.constants import ROLE_ADMIN, ROLE_DRIVER, ROLE_USER


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    @staticmethod
    def _hash_password(password: str) -> str:
        salt = os.urandom(16)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
        return f"{salt.hex()}${digest.hex()}"

    @staticmethod
    def _verify_password(password: str, password_hash: str) -> bool:
        try:
            salt_hex, digest_hex = password_hash.split("$", 1)
        except ValueError:
            return False

        salt = bytes.fromhex(salt_hex)
        expected = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
        return expected.hex() == digest_hex

    def register(
        self,
        full_name: str,
        address: str,
        phone: str,
        email: str,
        password: str,
        confirm_password: str,
    ) -> tuple[bool, str, User | None]:
        ok, message = ValidationService.validate_registration(
            full_name, address, phone, email, password, confirm_password
        )
        if not ok:
            return False, message, None

        email = email.strip().lower()
        existing = self.user_repo.find_by_email(email)
        if existing:
            return False, "An account already exists with this email.", None

        user = self.user_repo.create_user(
            full_name=full_name.strip(),
            address=address.strip(),
            phone=phone.strip(),
            email=email,
            password_hash=self._hash_password(password),
            role=ROLE_USER,
        )
        return True, "Registration successful.", user

    def login(self, email: str, password: str) -> tuple[bool, str, User | None]:
        email = email.strip().lower()
        user = self.user_repo.find_by_email(email)
        if user is None:
            return False, "No account found for this email.", None

        if not self._verify_password(password, user.password_hash):
            return False, "Invalid password.", None

        return True, "Login successful.", user

    def create_admin(
        self,
        full_name: str,
        address: str,
        phone: str,
        email: str,
        password: str,
    ) -> User:
        email = email.strip().lower()
        existing = self.user_repo.find_by_email(email)
        if existing:
            return existing

        return self.user_repo.create_user(
            full_name=full_name.strip(),
            address=address.strip(),
            phone=phone.strip(),
            email=email,
            password_hash=self._hash_password(password),
            role=ROLE_ADMIN,
        )

    def create_driver(
        self,
        full_name: str,
        address: str,
        phone: str,
        email: str,
        password: str,
    ) -> User:
        email = email.strip().lower()
        existing = self.user_repo.find_by_email(email)
        if existing:
            return existing

        return self.user_repo.create_user(
            full_name=full_name.strip(),
            address=address.strip(),
            phone=phone.strip(),
            email=email,
            password_hash=self._hash_password(password),
            role=ROLE_DRIVER,
        )
