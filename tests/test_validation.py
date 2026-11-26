from __future__ import annotations

import unittest

from app.services.validation_service import ValidationService
from app.utils.constants import CAR_TYPES


class TestValidationService(unittest.TestCase):
    def test_valid_email(self):
        self.assertTrue(ValidationService.is_valid_email("user@example.com"))
        self.assertFalse(ValidationService.is_valid_email("invalid-email"))

    def test_valid_phone(self):
        self.assertTrue(ValidationService.is_valid_phone("123456789"))
        self.assertFalse(ValidationService.is_valid_phone("12ab56"))

    def test_booking_validation(self):
        ok, _, distance = ValidationService.validate_booking_fields(
            "A", "B", "2026-12-21", "09:30", "12.5", "Standard", CAR_TYPES
        )
        self.assertTrue(ok)
        self.assertEqual(distance, 12.5)

        ok, _, _ = ValidationService.validate_booking_fields(
            "A", "A", "2026-12-21", "09:30", "12.5", "Standard", CAR_TYPES
        )
        self.assertFalse(ok)

        ok, msg, _ = ValidationService.validate_booking_fields(
            "A", "B", "21-12-2026", "09:30", "12.5", "Standard", CAR_TYPES
        )
        self.assertFalse(ok)
        self.assertIn("yyyy-mm-dd", msg.lower())

    def test_registration_requires_address(self):
        ok, msg = ValidationService.validate_registration(
            full_name="Alice",
            address="",
            phone="1234567890",
            email="alice@example.com",
            password="secret123",
            confirm_password="secret123",
        )
        self.assertFalse(ok)
        self.assertIn("address", msg.lower())


if __name__ == "__main__":
    unittest.main()
