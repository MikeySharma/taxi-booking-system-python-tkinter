from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "taxi_booking.db"

APP_TITLE = "Taxi Booking System"
APP_GEOMETRY = "1100x700"
