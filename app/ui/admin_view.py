from __future__ import annotations

from tkinter import messagebox
from tkinter import ttk

from app.utils.constants import BOOKING_STATUSES, ROLE_ADMIN
from app.utils.helpers import format_currency


class AdminView(ttk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.driver_id_by_label: dict[str, int] = {}

        if self.app.current_user is None:
            messagebox.showwarning("Session", "Please login first.")
            self.app.show_login()
            return
        if self.app.current_user.role != ROLE_ADMIN:
            messagebox.showerror("Access denied", "Admin access only.")
            self.app.show_dashboard()
            return

        ttk.Label(self, text="Admin Panel", font=("Arial", 16, "bold")).pack(anchor="w", pady=(0, 8))

        top = ttk.Frame(self)
        top.pack(fill="x", pady=(0, 8))

        ttk.Button(top, text="Refresh", command=self.refresh).pack(side="left")

        ttk.Label(top, text="Status:").pack(side="left", padx=(14, 6))
        self.status_box = ttk.Combobox(top, values=BOOKING_STATUSES, state="readonly", width=16)
        self.status_box.pack(side="left")
        self.status_box.set(BOOKING_STATUSES[1])
        ttk.Button(top, text="Update Status", command=self.update_selected_status).pack(side="left", padx=8)

        ttk.Label(top, text="Driver:").pack(side="left", padx=(14, 6))
        self.driver_box = ttk.Combobox(top, state="readonly", width=30)
        self.driver_box.pack(side="left")
        ttk.Button(top, text="Assign Driver", command=self.assign_selected_driver).pack(side="left", padx=8)

        ttk.Button(top, text="Back", command=self.app.show_dashboard).pack(side="right")

        columns = (
            "id",
            "customer",
            "pickup",
            "dropoff",
            "date",
            "time",
            "distance",
            "car",
            "driver",
            "fare",
            "status",
            "created",
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
            "driver": "Assigned Driver",
            "fare": "Fare",
            "status": "Status",
            "created": "Created",
        }
        widths = {
            "id": 55,
            "customer": 190,
            "pickup": 120,
            "dropoff": 120,
            "date": 95,
            "time": 80,
            "distance": 90,
            "car": 85,
            "driver": 180,
            "fare": 85,
            "status": 100,
            "created": 145,
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")

        self.refresh_drivers()
        self.refresh()

    def refresh_drivers(self):
        drivers = self.app.user_repo.list_drivers()
        self.driver_id_by_label = {
            f"{driver.full_name} ({driver.email})": driver.id for driver in drivers
        }
        labels = list(self.driver_id_by_label.keys())
        self.driver_box["values"] = labels
        if labels:
            self.driver_box.set(labels[0])
        else:
            self.driver_box.set("")

    def refresh(self):
        self.refresh_drivers()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for booking in self.app.booking_service.get_all_bookings():
            customer_name = booking.user_name or f"User #{booking.user_id}"
            customer_email = booking.user_email or "-"
            driver_label = (
                f"{booking.driver_name} ({booking.driver_email})"
                if booking.driver_name and booking.driver_email
                else "Unassigned"
            )

            self.tree.insert(
                "",
                "end",
                values=(
                    booking.id,
                    f"{customer_name} ({customer_email})",
                    booking.pickup_location,
                    booking.dropoff_location,
                    booking.scheduled_date,
                    booking.scheduled_time,
                    booking.distance_km,
                    booking.car_type,
                    driver_label,
                    format_currency(booking.fare_amount),
                    booking.booking_status,
                    booking.created_at,
                ),
            )

    def _selected_booking_id(self) -> int | None:
        selected = self.tree.selection()
        if not selected:
            return None
        return int(self.tree.item(selected[0])["values"][0])

    def update_selected_status(self):
        booking_id = self._selected_booking_id()
        if booking_id is None:
            messagebox.showwarning("Admin", "Select a booking first.")
            return

        status = self.status_box.get()
        ok, message = self.app.booking_service.admin_update_status(booking_id, status)
        if not ok:
            messagebox.showerror("Admin", message)
            return

        messagebox.showinfo("Admin", message)
        self.refresh()

    def assign_selected_driver(self):
        booking_id = self._selected_booking_id()
        if booking_id is None:
            messagebox.showwarning("Admin", "Select a booking first.")
            return

        label = self.driver_box.get().strip()
        driver_id = self.driver_id_by_label.get(label)
        if driver_id is None:
            messagebox.showwarning("Admin", "Select a valid driver.")
            return

        ok, message = self.app.booking_service.assign_driver(booking_id, driver_id)
        if not ok:
            messagebox.showerror("Assign Driver", message)
            return

        messagebox.showinfo("Assign Driver", message)
        self.refresh()
