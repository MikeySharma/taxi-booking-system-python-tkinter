from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.db.connection import Database
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.utils.constants import ROLE_DRIVER


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp_dir.name) / "auth_test.db"
        self.db = Database(self.db_path)
        self.db.init_schema()
        self.user_repo = UserRepository(self.db)
        self.auth = AuthService(self.user_repo)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_register_and_login_success(self):
        ok, _, user = self.auth.register(
            "Alice Doe",
            "Kathmandu",
            "1234567890",
            "alice@example.com",
            "secret123",
            "secret123",
        )
        self.assertTrue(ok)
        self.assertIsNotNone(user)

        ok, _, logged_user = self.auth.login("alice@example.com", "secret123")
        self.assertTrue(ok)
        self.assertIsNotNone(logged_user)
        self.assertEqual(logged_user.email, "alice@example.com")

    def test_duplicate_email_rejected(self):
        self.auth.register(
            "Alice Doe",
            "Kathmandu",
            "1234567890",
            "alice@example.com",
            "secret123",
            "secret123",
        )
        ok, msg, _ = self.auth.register(
            "Alice 2",
            "Bhaktapur",
            "1234567899",
            "alice@example.com",
            "password123",
            "password123",
        )
        self.assertFalse(ok)
        self.assertIn("already exists", msg.lower())

    def test_wrong_password_fails(self):
        self.auth.register(
            "Alice Doe",
            "Kathmandu",
            "1234567890",
            "alice@example.com",
            "secret123",
            "secret123",
        )
        ok, _, _ = self.auth.login("alice@example.com", "wrong")
        self.assertFalse(ok)

    def test_create_driver(self):
        driver = self.auth.create_driver(
            "Driver One",
            "Taxi Stand",
            "9800000001",
            "driver1@taxi.local",
            "Driver@123",
        )
        self.assertEqual(driver.role, ROLE_DRIVER)


if __name__ == "__main__":
    unittest.main()
