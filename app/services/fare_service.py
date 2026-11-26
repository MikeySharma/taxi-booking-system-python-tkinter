from __future__ import annotations

from app.utils.constants import BASE_FARE, CAR_TYPE_MULTIPLIER, PER_KM_RATE


class FareService:
    def calculate_fare(self, distance_km: float, car_type: str, surge_multiplier: float = 1.0) -> float:
        if distance_km <= 0:
            raise ValueError("Distance must be greater than zero.")

        car_multiplier = CAR_TYPE_MULTIPLIER.get(car_type)
        if car_multiplier is None:
            raise ValueError("Invalid car type.")

        if surge_multiplier <= 0:
            raise ValueError("Surge multiplier must be greater than zero.")

        fare = (BASE_FARE + (distance_km * PER_KM_RATE)) * car_multiplier * surge_multiplier
        return round(fare, 2)
