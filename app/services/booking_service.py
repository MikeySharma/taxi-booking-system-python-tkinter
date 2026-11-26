from __future__ import annotations

from app.models.booking import Booking
from app.repositories.booking_repository import BookingRepository
from app.repositories.user_repository import UserRepository
from app.services.fare_service import FareService
from app.services.validation_service import ValidationService
from app.utils.constants import (
    BOOKING_CANCELLED,
    BOOKING_PENDING,
    BOOKING_STATUSES,
    CAR_TYPES,
    ROLE_DRIVER,
)


class BookingService:
    def __init__(
        self,
        booking_repo: BookingRepository,
        fare_service: FareService,
        user_repo: UserRepository | None = None,
    ):
        self.booking_repo = booking_repo
        self.fare_service = fare_service
        self.user_repo = user_repo

    def create_booking(
        self,
        user_id: int,
        pickup_location: str,
        dropoff_location: str,
        scheduled_date: str,
        scheduled_time: str,
        distance_text: str,
        car_type: str,
    ) -> tuple[bool, str, Booking | None]:
        ok, message, distance_km = ValidationService.validate_booking_fields(
            pickup_location,
            dropoff_location,
            scheduled_date,
            scheduled_time,
            distance_text,
            car_type,
            CAR_TYPES,
        )
        if not ok or distance_km is None:
            return False, message, None

        fare_amount = self.fare_service.calculate_fare(distance_km, car_type)
        booking = self.booking_repo.create_booking(
            user_id=user_id,
            pickup_location=pickup_location.strip(),
            dropoff_location=dropoff_location.strip(),
            scheduled_date=scheduled_date.strip(),
            scheduled_time=scheduled_time.strip(),
            distance_km=distance_km,
            car_type=car_type,
            fare_amount=fare_amount,
        )
        return True, "Booking created successfully.", booking

    def update_booking(
        self,
        user_id: int,
        booking_id: int,
        pickup_location: str,
        dropoff_location: str,
        scheduled_date: str,
        scheduled_time: str,
        distance_text: str,
        car_type: str,
    ) -> tuple[bool, str, Booking | None]:
        ok, message, distance_km = ValidationService.validate_booking_fields(
            pickup_location,
            dropoff_location,
            scheduled_date,
            scheduled_time,
            distance_text,
            car_type,
            CAR_TYPES,
        )
        if not ok or distance_km is None:
            return False, message, None

        current_booking = self.booking_repo.get_by_id(booking_id)
        if current_booking and current_booking.assigned_driver_id is not None:
            has_overlap = self.booking_repo.has_driver_overlap(
                driver_id=current_booking.assigned_driver_id,
                scheduled_date=scheduled_date.strip(),
                scheduled_time=scheduled_time.strip(),
                exclude_booking_id=booking_id,
            )
            if has_overlap:
                return (
                    False,
                    "Selected date/time overlaps with the assigned driver's schedule.",
                    None,
                )

        fare_amount = self.fare_service.calculate_fare(distance_km, car_type)
        updated = self.booking_repo.update_booking_details(
            booking_id=booking_id,
            user_id=user_id,
            pickup_location=pickup_location.strip(),
            dropoff_location=dropoff_location.strip(),
            scheduled_date=scheduled_date.strip(),
            scheduled_time=scheduled_time.strip(),
            distance_km=distance_km,
            car_type=car_type,
            fare_amount=fare_amount,
        )
        if not updated:
            return (
                False,
                "Booking update failed. Only your pending bookings can be updated.",
                None,
            )

        booking = self.booking_repo.get_by_id(booking_id)
        return True, "Booking updated successfully.", booking

    def cancel_booking(self, user_id: int, booking_id: int) -> tuple[bool, str]:
        booking = self.booking_repo.get_by_id(booking_id)
        if booking is None:
            return False, "Booking not found."
        if booking.user_id != user_id:
            return False, "You cannot cancel someone else's booking."
        if booking.booking_status != BOOKING_PENDING:
            return False, "Only pending bookings can be cancelled."

        cancelled = self.booking_repo.update_status(booking_id, "cancelled")
        if not cancelled:
            return False, "Unable to cancel booking right now."
        return True, "Booking cancelled successfully."

    def estimate_fare(self, distance_text: str, car_type: str) -> tuple[bool, str, float | None]:
        try:
            distance_km = float(distance_text)
            fare = self.fare_service.calculate_fare(distance_km, car_type)
            return True, "Fare estimated.", fare
        except ValueError as exc:
            return False, str(exc), None

    def get_user_bookings(self, user_id: int) -> list[Booking]:
        return self.booking_repo.list_by_user(user_id)

    def get_all_bookings(self) -> list[Booking]:
        return self.booking_repo.list_all_with_user()

    def get_driver_bookings(self, driver_id: int) -> list[Booking]:
        return self.booking_repo.list_assigned_to_driver(driver_id)

    def assign_driver(self, booking_id: int, driver_id: int) -> tuple[bool, str]:
        if self.user_repo is None:
            return False, "User repository is not configured."

        driver = self.user_repo.find_by_id(driver_id)
        if driver is None or driver.role != ROLE_DRIVER:
            return False, "Selected driver is invalid."

        booking = self.booking_repo.get_by_id(booking_id)
        if booking is None:
            return False, "Booking not found."
        if booking.booking_status == BOOKING_CANCELLED:
            return False, "Cannot assign driver to a cancelled booking."

        has_overlap = self.booking_repo.has_driver_overlap(
            driver_id=driver_id,
            scheduled_date=booking.scheduled_date,
            scheduled_time=booking.scheduled_time,
            exclude_booking_id=booking.id,
        )
        if has_overlap:
            return (
                False,
                "Driver already has another booking at the same date and time.",
            )

        assigned = self.booking_repo.assign_driver(booking_id, driver_id)
        if not assigned:
            return False, "Failed to assign driver."
        return True, "Driver assigned successfully."

    def admin_update_status(self, booking_id: int, status: str) -> tuple[bool, str]:
        if status not in BOOKING_STATUSES:
            return False, "Invalid booking status."
        updated = self.booking_repo.update_status(booking_id, status)
        if not updated:
            return False, "Booking not found."
        return True, "Booking status updated."
