from __future__ import annotations

import unittest

from app.services.fare_service import FareService


class TestFareService(unittest.TestCase):
    def setUp(self):
        self.service = FareService()

    def test_standard_fare(self):
        fare = self.service.calculate_fare(10, "Standard")
        self.assertEqual(fare, 30.0)

    def test_premium_fare(self):
        fare = self.service.calculate_fare(10, "Premium")
        self.assertEqual(fare, 45.0)

    def test_invalid_distance(self):
        with self.assertRaises(ValueError):
            self.service.calculate_fare(0, "Standard")


if __name__ == "__main__":
    unittest.main()
