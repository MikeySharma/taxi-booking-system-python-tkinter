from __future__ import annotations

from tkinter import messagebox
from tkinter import ttk

from app.utils.constants import ROLE_DRIVER
from app.utils.helpers import format_currency


class DriverTripsView(ttk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        if self.app.current_user is None:
            messagebox.showwarning("Session", "Please login first.")
            self.app.show_login()
            return
        if self.app.current_user.role != ROLE_DRIVER:
            messagebox.showerror("Access denied", "Driver access only.")
            self.app.show_dashboard()
            return

        ttk.Label(self, text="My Assigned Trips", font=("Arial", 16, "bold")).pack(
            anchor="w", pady=(0, 8)
        )

        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=(0, 8))
        ttk.Button(actions, text="Refresh", command=self.refresh).pack(side="left")
        ttk.Button(actions, text="Back", command=self.app.show_dashboard).pack(side="right")

        columns = (
            "id",
            "customer",
            "pickup",
            "dropoff",
            "date",
            "time",
            "distance",
            "car",
            "fare",
            "status",
        )
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=22)
        self.tree.pack(fill="both", expand=True)

        headings = {
            "id": "ID",
            "customer": "Customer",
            "pickup": "Pickup",
            "dropoff": "Drop-off",
            "date": "Date",
            "time": "Time",
            "distance": "Distance(km)",
            "car": "Car",
            "fare": "Fare",
            "status": "Status",
        }
        widths = {
            "id": 60,
            "customer": 180,
            "pickup": 130,
            "dropoff": 130,
            "date": 100,
            "time": 80,
            "distance": 95,
            "car": 90,
            "fare": 90,
            "status": 100,
        }
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")

        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        trips = self.app.booking_service.get_driver_bookings(self.app.current_user.id)
        for trip in trips:
            customer = trip.user_name or f"User #{trip.user_id}"
            self.tree.insert(
                "",
                "end",
                values=(
                    trip.id,
                    customer,
                    trip.pickup_location,
                    trip.dropoff_location,
                    trip.scheduled_date,
                    trip.scheduled_time,
                    trip.distance_km,
                    trip.car_type,
                    format_currency(trip.fare_amount),
                    trip.booking_status,
                ),
            )
