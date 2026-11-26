from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from app.models.booking import Booking
from app.utils.constants import BOOKING_PENDING, CAR_TYPES
from app.utils.helpers import format_currency


class EditBookingDialog(tk.Toplevel):
    def __init__(self, parent, booking: Booking, on_save):
        super().__init__(parent)
        self.title(f"Edit Booking #{booking.id}")
        self.resizable(False, False)
        self.booking = booking
        self.on_save = on_save

        form = ttk.Frame(self, padding=12)
        form.pack(fill="both", expand=True)

        ttk.Label(form, text="Pickup location").grid(row=0, column=0, sticky="w", pady=5, padx=(0, 8))
        self.pickup_entry = ttk.Entry(form, width=40)
        self.pickup_entry.grid(row=0, column=1, pady=5)
        self.pickup_entry.insert(0, booking.pickup_location)

        ttk.Label(form, text="Drop-off location").grid(row=1, column=0, sticky="w", pady=5, padx=(0, 8))
        self.dropoff_entry = ttk.Entry(form, width=40)
        self.dropoff_entry.grid(row=1, column=1, pady=5)
        self.dropoff_entry.insert(0, booking.dropoff_location)

        ttk.Label(form, text="Distance (km)").grid(row=2, column=0, sticky="w", pady=5, padx=(0, 8))
        self.distance_entry = ttk.Entry(form, width=40)
        self.distance_entry.grid(row=2, column=1, pady=5)
        self.distance_entry.insert(0, str(booking.distance_km))

        ttk.Label(form, text="Date (YYYY-MM-DD)").grid(row=3, column=0, sticky="w", pady=5, padx=(0, 8))
        self.date_entry = ttk.Entry(form, width=40)
        self.date_entry.grid(row=3, column=1, pady=5)
        self.date_entry.insert(0, booking.scheduled_date)

        ttk.Label(form, text="Time (HH:MM)").grid(row=4, column=0, sticky="w", pady=5, padx=(0, 8))
        self.time_entry = ttk.Entry(form, width=40)
        self.time_entry.grid(row=4, column=1, pady=5)
        self.time_entry.insert(0, booking.scheduled_time)

        ttk.Label(form, text="Car type").grid(row=5, column=0, sticky="w", pady=5, padx=(0, 8))
        self.car_type_box = ttk.Combobox(form, values=CAR_TYPES, state="readonly", width=37)
        self.car_type_box.grid(row=5, column=1, pady=5)
        self.car_type_box.set(booking.car_type)

        btns = ttk.Frame(form)
        btns.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        ttk.Button(btns, text="Save", command=self._save).pack(side="left")
        ttk.Button(btns, text="Cancel", command=self.destroy).pack(side="left", padx=8)

        self.transient(parent)
        self.grab_set()

    def _save(self):
        ok = self.on_save(
            self.booking.id,
            self.pickup_entry.get(),
            self.dropoff_entry.get(),
            self.date_entry.get(),
            self.time_entry.get(),
            self.distance_entry.get(),
            self.car_type_box.get(),
        )
        if ok:
            self.destroy()


class BookingListView(ttk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.bookings_by_id: dict[int, Booking] = {}

        if self.app.current_user is None:
            messagebox.showwarning("Session", "Please login first.")
            self.app.show_login()
            return

        ttk.Label(self, text="My Bookings", font=("Arial", 16, "bold")).pack(anchor="w", pady=(0, 8))

        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=(0, 8))

        ttk.Button(actions, text="Refresh", command=self.refresh_bookings).pack(side="left")
        ttk.Button(actions, text="Edit Selected", command=self.on_edit_selected).pack(side="left", padx=8)
        ttk.Button(actions, text="Cancel Selected", command=self.on_cancel_selected).pack(side="left")
        ttk.Button(actions, text="Back", command=self.app.show_dashboard).pack(side="right")

        columns = (
            "id",
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
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=20)
        self.tree.pack(fill="both", expand=True)

        headings = {
            "id": "ID",
            "pickup": "Pickup",
            "dropoff": "Drop-off",
            "date": "Date",
            "time": "Time",
            "distance": "Distance(km)",
            "car": "Car Type",
            "driver": "Assigned Driver",
            "fare": "Fare",
            "status": "Status",
            "created": "Created",
        }
        widths = {
            "id": 60,
            "pickup": 130,
            "dropoff": 130,
            "date": 100,
            "time": 80,
            "distance": 95,
            "car": 95,
            "driver": 180,
            "fare": 90,
            "status": 100,
            "created": 150,
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")

        self.refresh_bookings()

    def refresh_bookings(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        bookings = self.app.booking_service.get_user_bookings(self.app.current_user.id)
        self.bookings_by_id = {b.id: b for b in bookings}

        for booking in bookings:
            self.tree.insert(
                "",
                "end",
                values=(
                    booking.id,
                    booking.pickup_location,
                    booking.dropoff_location,
                    booking.scheduled_date,
                    booking.scheduled_time,
                    booking.distance_km,
                    booking.car_type,
                    booking.driver_name or "-",
                    format_currency(booking.fare_amount),
                    booking.booking_status,
                    booking.created_at,
                ),
            )

    def _get_selected_booking_id(self) -> int | None:
        selected = self.tree.selection()
        if not selected:
            return None
        item = self.tree.item(selected[0])
        return int(item["values"][0])

    def on_cancel_selected(self):
        booking_id = self._get_selected_booking_id()
        if booking_id is None:
            messagebox.showwarning("Booking", "Select a booking first.")
            return

        confirmed = messagebox.askyesno("Confirm", "Cancel selected booking?")
        if not confirmed:
            return

        ok, message = self.app.booking_service.cancel_booking(self.app.current_user.id, booking_id)
        if not ok:
            messagebox.showerror("Cancel failed", message)
            return

        messagebox.showinfo("Booking", message)
        self.refresh_bookings()

    def on_edit_selected(self):
        booking_id = self._get_selected_booking_id()
        if booking_id is None:
            messagebox.showwarning("Booking", "Select a booking first.")
            return

        booking = self.bookings_by_id.get(booking_id)
        if booking is None:
            messagebox.showerror("Booking", "Booking not found.")
            return
        if booking.booking_status != BOOKING_PENDING:
            messagebox.showwarning("Booking", "Only pending bookings can be edited.")
            return

        EditBookingDialog(self, booking, self._save_booking_edits)

    def _save_booking_edits(
        self,
        booking_id: int,
        pickup_location: str,
        dropoff_location: str,
        scheduled_date: str,
        scheduled_time: str,
        distance_text: str,
        car_type: str,
    ) -> bool:
        ok, message, _ = self.app.booking_service.update_booking(
            user_id=self.app.current_user.id,
            booking_id=booking_id,
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            scheduled_date=scheduled_date,
            scheduled_time=scheduled_time,
            distance_text=distance_text,
            car_type=car_type,
        )
        if not ok:
            messagebox.showerror("Update failed", message)
            return False

        messagebox.showinfo("Booking", message)
        self.refresh_bookings()
        return True
