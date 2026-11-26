from __future__ import annotations

from tkinter import messagebox
from tkinter import ttk

from app.utils.constants import CAR_TYPES
from app.utils.helpers import format_currency


class BookingFormView(ttk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        if self.app.current_user is None:
            messagebox.showwarning("Session", "Please login first.")
            self.app.show_login()
            return

        ttk.Label(self, text="Create Booking", font=("Arial", 16, "bold")).pack(anchor="w", pady=(0, 12))

        form = ttk.Frame(self)
        form.pack(fill="x")

        ttk.Label(form, text="Pickup location").grid(row=0, column=0, sticky="w", pady=6, padx=(0, 8))
        self.pickup_entry = ttk.Entry(form, width=48)
        self.pickup_entry.grid(row=0, column=1, sticky="w", pady=6)

        ttk.Label(form, text="Drop-off location").grid(row=1, column=0, sticky="w", pady=6, padx=(0, 8))
        self.dropoff_entry = ttk.Entry(form, width=48)
        self.dropoff_entry.grid(row=1, column=1, sticky="w", pady=6)

        ttk.Label(form, text="Date (YYYY-MM-DD)").grid(row=2, column=0, sticky="w", pady=6, padx=(0, 8))
        self.date_entry = ttk.Entry(form, width=48)
        self.date_entry.grid(row=2, column=1, sticky="w", pady=6)

        ttk.Label(form, text="Time (HH:MM)").grid(row=3, column=0, sticky="w", pady=6, padx=(0, 8))
        self.time_entry = ttk.Entry(form, width=48)
        self.time_entry.grid(row=3, column=1, sticky="w", pady=6)

        ttk.Label(form, text="Distance (km)").grid(row=4, column=0, sticky="w", pady=6, padx=(0, 8))
        self.distance_entry = ttk.Entry(form, width=48)
        self.distance_entry.grid(row=4, column=1, sticky="w", pady=6)

        ttk.Label(form, text="Car type").grid(row=5, column=0, sticky="w", pady=6, padx=(0, 8))
        self.car_type_box = ttk.Combobox(form, values=CAR_TYPES, state="readonly", width=45)
        self.car_type_box.grid(row=5, column=1, sticky="w", pady=6)
        self.car_type_box.set(CAR_TYPES[0])

        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=14)

        ttk.Button(actions, text="Estimate Fare", command=self.on_estimate_fare).pack(side="left")
        ttk.Button(actions, text="Create Booking", command=self.on_create_booking).pack(side="left", padx=8)
        ttk.Button(actions, text="Back", command=self.app.show_dashboard).pack(side="left")

        self.fare_label = ttk.Label(self, text="Estimated Fare: -", font=("Arial", 12, "bold"))
        self.fare_label.pack(anchor="w")

    def on_estimate_fare(self):
        ok, message, fare = self.app.booking_service.estimate_fare(
            self.distance_entry.get(), self.car_type_box.get()
        )
        if not ok or fare is None:
            messagebox.showerror("Estimate failed", message)
            return

        self.fare_label.config(text=f"Estimated Fare: {format_currency(fare)}")

    def on_create_booking(self):
        ok, message, booking = self.app.booking_service.create_booking(
            user_id=self.app.current_user.id,
            pickup_location=self.pickup_entry.get(),
            dropoff_location=self.dropoff_entry.get(),
            scheduled_date=self.date_entry.get(),
            scheduled_time=self.time_entry.get(),
            distance_text=self.distance_entry.get(),
            car_type=self.car_type_box.get(),
        )
        if not ok or booking is None:
            messagebox.showerror("Booking failed", message)
            return

        messagebox.showinfo("Booking", f"Booking #{booking.id} created successfully.")
        self.pickup_entry.delete(0, "end")
        self.dropoff_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.time_entry.delete(0, "end")
        self.distance_entry.delete(0, "end")
        self.fare_label.config(text="Estimated Fare: -")
