# Taxi Booking System (Python Tkinter)

Desktop Taxi Booking System built with Python, Tkinter, SQLite, and OOP.

## Features

- Customer, driver, and admin login flows
- User registration with name, address, phone, email
- Taxi booking with pickup/drop-off, date, time, distance, car type
- Fare estimation and booking history (edit/cancel pending bookings)
- Driver panel to view assigned trips
- Admin panel to view all bookings, assign drivers, and update statuses
- Driver overlap prevention (same date/time conflict check)
- SQLite data persistence
- Unit tests for core services

## Project Structure

```text
app/
  main.py
  config.py
  ui/
  models/
  services/
  repositories/
  db/
  utils/
tests/
```

## Run the Application

From project root:

```bash
uv venv --python 3.14 .venv
uv run -m app.main
```

## Default Admin Account

- Email: `admin@taxi.local`
- Password: `Admin@123`

## Seeded Demo Users

- Email: `alice@student.local` | Password: `Alice@123`
- Email: `bob@student.local` | Password: `Bob@12345`
- Driver: `driver1@taxi.local` | Password: `Driver@123`
- Driver: `driver2@taxi.local` | Password: `Driver@123`

## Run Tests

```bash
uv run -m unittest discover -s tests -v
```

## Exam Readiness Checklist

```bash
uv run python scripts/exam_readiness_check.py --run-tests
```

This validates key project files/features and stores test output in:

- `report_evidence/testing/unit-test-output.txt`

Report evidence structure is available in:

- `report_evidence/`

## LaTeX Project Report

- Source: `report/main.tex`
- Assets folder: `report/assets/`

Build commands are documented in `report/README.md`.
