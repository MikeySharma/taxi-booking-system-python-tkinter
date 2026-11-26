from __future__ import annotations


def format_currency(value: float) -> str:
    return f"${value:,.2f}"


def safe_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
