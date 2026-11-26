from __future__ import annotations

from app.db.connection import Database
from app.models.booking import Booking


class BookingRepository:
    def __init__(self, db: Database):
        self.db = db

    def create_booking(
        self,
        user_id: int,
        pickup_location: str,
        dropoff_location: str,
        scheduled_date: str,
        scheduled_time: str,
        distance_km: float,
        car_type: str,
        fare_amount: float,
    ) -> Booking:
        booking_id = self.db.execute(
            """
            INSERT INTO bookings (
                user_id, pickup_location, dropoff_location,
                scheduled_date, scheduled_time,
                distance_km, car_type, fare_amount, booking_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending')
            """,
            (
                user_id,
                pickup_location,
                dropoff_location,
                scheduled_date,
                scheduled_time,
                distance_km,
                car_type,
                fare_amount,
            ),
        )
        booking = self.get_by_id(booking_id)
        if booking is None:
            raise RuntimeError("Failed to create booking")
        return booking

    def get_by_id(self, booking_id: int) -> Booking | None:
        row = self.db.fetch_one("SELECT * FROM bookings WHERE id = ?", (booking_id,))
        return Booking.from_row(row) if row else None

    def list_by_user(self, user_id: int) -> list[Booking]:
        rows = self.db.fetch_all(
            """
            SELECT
                b.*,
                d.email AS driver_email,
                d.full_name AS driver_name
            FROM bookings b
            LEFT JOIN users d ON d.id = b.assigned_driver_id
            WHERE b.user_id = ?
            ORDER BY b.created_at DESC
            """,
            (user_id,),
        )
        return [Booking.from_row(row) for row in rows]

    def list_all_with_user(self) -> list[Booking]:
        rows = self.db.fetch_all(
            """
            SELECT
                b.*,
                u.email AS user_email,
                u.full_name AS user_name,
                d.email AS driver_email,
                d.full_name AS driver_name
            FROM bookings b
            INNER JOIN users u ON u.id = b.user_id
            LEFT JOIN users d ON d.id = b.assigned_driver_id
            ORDER BY b.created_at DESC
            """
        )
        return [Booking.from_row(row) for row in rows]

    def list_assigned_to_driver(self, driver_id: int) -> list[Booking]:
        rows = self.db.fetch_all(
            """
            SELECT
                b.*,
                u.email AS user_email,
                u.full_name AS user_name,
                d.email AS driver_email,
                d.full_name AS driver_name
            FROM bookings b
            INNER JOIN users u ON u.id = b.user_id
            LEFT JOIN users d ON d.id = b.assigned_driver_id
            WHERE b.assigned_driver_id = ?
            ORDER BY b.scheduled_date ASC, b.scheduled_time ASC
            """,
            (driver_id,),
        )
        return [Booking.from_row(row) for row in rows]

    def update_status(self, booking_id: int, status: str) -> bool:
        row_count = self.db.execute_non_query(
            """
            UPDATE bookings
            SET booking_status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (status, booking_id),
        )
        return row_count > 0

    def update_booking_details(
        self,
        booking_id: int,
        user_id: int,
        pickup_location: str,
        dropoff_location: str,
        scheduled_date: str,
        scheduled_time: str,
        distance_km: float,
        car_type: str,
        fare_amount: float,
    ) -> bool:
        row_count = self.db.execute_non_query(
            """
            UPDATE bookings
            SET
                pickup_location = ?,
                dropoff_location = ?,
                scheduled_date = ?,
                scheduled_time = ?,
                distance_km = ?,
                car_type = ?,
                fare_amount = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE
                id = ?
                AND user_id = ?
                AND booking_status = 'pending'
            """,
            (
                pickup_location,
                dropoff_location,
                scheduled_date,
                scheduled_time,
                distance_km,
                car_type,
                fare_amount,
                booking_id,
                user_id,
            ),
        )
        return row_count > 0

    def assign_driver(self, booking_id: int, driver_id: int) -> bool:
        row_count = self.db.execute_non_query(
            """
            UPDATE bookings
            SET assigned_driver_id = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (driver_id, booking_id),
        )
        return row_count > 0

    def has_driver_overlap(
        self,
        driver_id: int,
        scheduled_date: str,
        scheduled_time: str,
        exclude_booking_id: int | None = None,
    ) -> bool:
        query = (
            """
            SELECT COUNT(1) AS booking_count
            FROM bookings
            WHERE
                assigned_driver_id = ?
                AND scheduled_date = ?
                AND scheduled_time = ?
                AND booking_status != 'cancelled'
            """
        )
        params: tuple = (driver_id, scheduled_date, scheduled_time)

        if exclude_booking_id is not None:
            query += " AND id != ?"
            params = (driver_id, scheduled_date, scheduled_time, exclude_booking_id)

        row = self.db.fetch_one(query, params)
        if row is None:
            return False
        return row["booking_count"] > 0
