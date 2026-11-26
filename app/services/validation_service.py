from __future__ import annotations

from datetime import datetime
import re


class ValidationService:
    EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    PHONE_PATTERN = re.compile(r"^[0-9]{7,15}$")

    @classmethod
    def is_valid_email(cls, email: str) -> bool:
        return bool(cls.EMAIL_PATTERN.match(email.strip()))

    @classmethod
    def is_valid_phone(cls, phone: str) -> bool:
        return bool(cls.PHONE_PATTERN.match(phone.strip()))

    @staticmethod
    def is_strong_password(password: str) -> bool:
        return len(password) >= 6

    @classmethod
    def validate_registration(
        cls,
        full_name: str,
        address: str,
        phone: str,
        email: str,
        password: str,
        confirm_password: str,
    ) -> tuple[bool, str]:
        if not full_name.strip():
            return False, "Full name is required."
        if not address.strip():
            return False, "Address is required."
        if not cls.is_valid_phone(phone):
            return False, "Phone must be numeric and 7-15 digits."
        if not cls.is_valid_email(email):
            return False, "Please enter a valid email address."
        if not cls.is_strong_password(password):
            return False, "Password must be at least 6 characters long."
        if password != confirm_password:
            return False, "Password and confirm password do not match."
        return True, "Validation successful."

    @staticmethod
    def validate_booking_fields(
        pickup_location: str,
        dropoff_location: str,
        scheduled_date: str,
        scheduled_time: str,
        distance_text: str,
        car_type: str,
        allowed_car_types: list[str],
    ) -> tuple[bool, str, float | None]:
        if not pickup_location.strip():
            return False, "Pickup location is required.", None
        if not dropoff_location.strip():
            return False, "Drop-off location is required.", None
        if pickup_location.strip().lower() == dropoff_location.strip().lower():
            return False, "Pickup and drop-off locations must be different.", None

        try:
            datetime.strptime(scheduled_date.strip(), "%Y-%m-%d")
        except ValueError:
            return False, "Date must be in YYYY-MM-DD format.", None

        try:
            datetime.strptime(scheduled_time.strip(), "%H:%M")
        except ValueError:
            return False, "Time must be in HH:MM (24-hour) format.", None

        try:
            distance_km = float(distance_text)
        except ValueError:
            return False, "Distance must be a number.", None

        if distance_km <= 0:
            return False, "Distance must be greater than 0.", None
        if car_type not in allowed_car_types:
            return False, "Please select a valid car type.", None

        return True, "Validation successful.", distance_km
