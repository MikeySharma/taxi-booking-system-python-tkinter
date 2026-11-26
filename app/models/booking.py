from __future__ import annotations

from dataclasses import dataclass
from sqlite3 import Row
from typing import Any


@dataclass(slots=True)
class Booking:
    id: int
    user_id: int
    assigned_driver_id: int | None
    pickup_location: str
    dropoff_location: str
    scheduled_date: str
    scheduled_time: str
    distance_km: float
    car_type: str
    fare_amount: float
    booking_status: str
    created_at: str
    updated_at: str
    user_email: str | None = None
    user_name: str | None = None
    driver_name: str | None = None
    driver_email: str | None = None

    @classmethod
    def from_row(cls, row: Row | dict[str, Any]) -> "Booking":
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            assigned_driver_id=row["assigned_driver_id"] if "assigned_driver_id" in row.keys() else None,
            pickup_location=row["pickup_location"],
            dropoff_location=row["dropoff_location"],
            scheduled_date=row["scheduled_date"] if "scheduled_date" in row.keys() else "1970-01-01",
            scheduled_time=row["scheduled_time"] if "scheduled_time" in row.keys() else "00:00",
            distance_km=row["distance_km"],
            car_type=row["car_type"],
            fare_amount=row["fare_amount"],
            booking_status=row["booking_status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            user_email=row["user_email"] if "user_email" in row.keys() else None,
            user_name=row["user_name"] if "user_name" in row.keys() else None,
            driver_name=row["driver_name"] if "driver_name" in row.keys() else None,
            driver_email=row["driver_email"] if "driver_email" in row.keys() else None,
        )
