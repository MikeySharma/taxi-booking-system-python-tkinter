from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.db.connection import Database
from app.repositories.booking_repository import BookingRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.booking_service import BookingService
from app.services.fare_service import FareService


class TestBookingService(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp_dir.name) / "booking_test.db"
        self.db = Database(self.db_path)
        self.db.init_schema()

        self.user_repo = UserRepository(self.db)
        self.booking_repo = BookingRepository(self.db)

        self.auth = AuthService(self.user_repo)
        self.booking_service = BookingService(self.booking_repo, FareService(), self.user_repo)

        _, _, self.user1 = self.auth.register(
            "User One",
            "Address 1",
            "1234567890",
            "user1@example.com",
            "secret123",
            "secret123",
        )
        _, _, self.user2 = self.auth.register(
            "User Two",
            "Address 2",
            "1234567891",
            "user2@example.com",
            "secret123",
            "secret123",
        )
        self.driver = self.auth.create_driver(
            "Driver One",
            "Stand A",
            "9800000001",
            "driver@example.com",
            "Driver@123",
        )

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_create_and_cancel_booking(self):
        ok, _, booking = self.booking_service.create_booking(
            self.user1.id,
            "Campus",
            "Airport",
            "2026-12-20",
            "10:00",
            "10",
            "Standard",
        )
        self.assertTrue(ok)
        self.assertIsNotNone(booking)

        ok, _ = self.booking_service.cancel_booking(self.user1.id, booking.id)
        self.assertTrue(ok)

    def test_non_owner_cannot_cancel_booking(self):
        ok, _, booking = self.booking_service.create_booking(
            self.user1.id,
            "Campus",
            "Airport",
            "2026-12-20",
            "11:00",
            "8",
            "Standard",
        )
        self.assertTrue(ok)

        ok, msg = self.booking_service.cancel_booking(self.user2.id, booking.id)
        self.assertFalse(ok)
        self.assertIn("cannot cancel", msg.lower())

    def test_update_pending_booking(self):
        ok, _, booking = self.booking_service.create_booking(
            self.user1.id,
            "Campus",
            "Airport",
            "2026-12-21",
            "08:00",
            "8",
            "Standard",
        )
        self.assertTrue(ok)

        ok, _, updated = self.booking_service.update_booking(
            self.user1.id,
            booking.id,
            "Campus",
            "City Center",
            "2026-12-21",
            "09:00",
            "12",
            "Premium",
        )
        self.assertTrue(ok)
        self.assertIsNotNone(updated)
        self.assertEqual(updated.dropoff_location, "City Center")
        self.assertEqual(updated.car_type, "Premium")

    def test_driver_overlap_prevented_on_assignment(self):
        ok1, _, booking1 = self.booking_service.create_booking(
            self.user1.id,
            "Campus",
            "Airport",
            "2026-12-22",
            "10:00",
            "7",
            "Standard",
        )
        ok2, _, booking2 = self.booking_service.create_booking(
            self.user2.id,
            "Mall",
            "Hospital",
            "2026-12-22",
            "10:00",
            "5",
            "Standard",
        )
        self.assertTrue(ok1)
        self.assertTrue(ok2)

        ok, _ = self.booking_service.assign_driver(booking1.id, self.driver.id)
        self.assertTrue(ok)

        ok, msg = self.booking_service.assign_driver(booking2.id, self.driver.id)
        self.assertFalse(ok)
        self.assertIn("same date and time", msg.lower())


if __name__ == "__main__":
    unittest.main()
