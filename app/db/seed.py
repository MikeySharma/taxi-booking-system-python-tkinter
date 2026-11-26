from __future__ import annotations

from app.db.connection import Database
from app.repositories.booking_repository import BookingRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.booking_service import BookingService
from app.services.fare_service import FareService
from app.utils.constants import (
    BOOKING_CANCELLED,
    BOOKING_COMPLETED,
    BOOKING_CONFIRMED,
    DEFAULT_ADMIN_ADDRESS,
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_FULL_NAME,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_ADMIN_PHONE,
)


def seed_admin(database: Database) -> None:
    user_repo = UserRepository(database)
    auth_service = AuthService(user_repo)

    existing = user_repo.find_by_email(DEFAULT_ADMIN_EMAIL)
    if existing:
        return

    auth_service.create_admin(
        full_name=DEFAULT_ADMIN_FULL_NAME,
        address=DEFAULT_ADMIN_ADDRESS,
        phone=DEFAULT_ADMIN_PHONE,
        email=DEFAULT_ADMIN_EMAIL,
        password=DEFAULT_ADMIN_PASSWORD,
    )


def seed_sample_data(database: Database) -> None:
    user_repo = UserRepository(database)
    booking_repo = BookingRepository(database)
    auth_service = AuthService(user_repo)
    booking_service = BookingService(booking_repo, FareService(), user_repo)

    sample_customers = [
        {
            "full_name": "Alice Student",
            "address": "Campus Hostel Block A",
            "phone": "9876543210",
            "email": "alice@student.local",
            "password": "Alice@123",
        },
        {
            "full_name": "Bob Student",
            "address": "Campus Hostel Block B",
            "phone": "9876543211",
            "email": "bob@student.local",
            "password": "Bob@12345",
        },
    ]

    sample_drivers = [
        {
            "full_name": "Ramesh Driver",
            "address": "Taxi Stand 1",
            "phone": "9800000001",
            "email": "driver1@taxi.local",
            "password": "Driver@123",
        },
        {
            "full_name": "Sita Driver",
            "address": "Taxi Stand 2",
            "phone": "9800000002",
            "email": "driver2@taxi.local",
            "password": "Driver@123",
        },
    ]

    created_customers = []
    for customer in sample_customers:
        _, _, user = auth_service.register(
            full_name=customer["full_name"],
            address=customer["address"],
            phone=customer["phone"],
            email=customer["email"],
            password=customer["password"],
            confirm_password=customer["password"],
        )
        if user is None:
            user = user_repo.find_by_email(customer["email"])
        if user is not None:
            created_customers.append(user)

    created_drivers = []
    for driver in sample_drivers:
        user = auth_service.create_driver(
            full_name=driver["full_name"],
            address=driver["address"],
            phone=driver["phone"],
            email=driver["email"],
            password=driver["password"],
        )
        created_drivers.append(user)

    if len(created_customers) < 2 or len(created_drivers) < 2:
        return

    # Avoid duplicate sample booking seeding when app starts multiple times.
    existing_bookings = booking_repo.list_all_with_user()
    if existing_bookings:
        return

    alice = created_customers[0]
    bob = created_customers[1]
    driver_1 = created_drivers[0]
    driver_2 = created_drivers[1]

    _, _, booking_1 = booking_service.create_booking(
        user_id=alice.id,
        pickup_location="University Gate",
        dropoff_location="City Center",
        scheduled_date="2026-12-20",
        scheduled_time="09:00",
        distance_text="7.5",
        car_type="Standard",
    )

    _, _, booking_2 = booking_service.create_booking(
        user_id=alice.id,
        pickup_location="Main Library",
        dropoff_location="Airport",
        scheduled_date="2026-12-20",
        scheduled_time="11:00",
        distance_text="15",
        car_type="Premium",
    )

    _, _, booking_3 = booking_service.create_booking(
        user_id=bob.id,
        pickup_location="Student Hostel",
        dropoff_location="Railway Station",
        scheduled_date="2026-12-21",
        scheduled_time="10:30",
        distance_text="10",
        car_type="SUV",
    )

    _, _, booking_4 = booking_service.create_booking(
        user_id=bob.id,
        pickup_location="Shopping Mall",
        dropoff_location="Hospital",
        scheduled_date="2026-12-21",
        scheduled_time="16:00",
        distance_text="5",
        car_type="Standard",
    )

    if booking_1 is not None:
        booking_service.assign_driver(booking_1.id, driver_1.id)
    if booking_2 is not None:
        booking_service.assign_driver(booking_2.id, driver_2.id)
        booking_repo.update_status(booking_2.id, BOOKING_CONFIRMED)
    if booking_3 is not None:
        booking_service.assign_driver(booking_3.id, driver_1.id)
        booking_repo.update_status(booking_3.id, BOOKING_COMPLETED)
    if booking_4 is not None:
        booking_repo.update_status(booking_4.id, BOOKING_CANCELLED)
