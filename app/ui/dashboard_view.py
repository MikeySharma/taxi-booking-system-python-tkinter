from __future__ import annotations

from tkinter import messagebox
from tkinter import ttk

from app.utils.constants import ROLE_ADMIN, ROLE_DRIVER, ROLE_USER


class DashboardView(ttk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        if self.app.current_user is None:
            messagebox.showwarning("Session", "Please login first.")
            self.app.show_login()
            return

        user = self.app.current_user

        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 12))

        ttk.Label(
            header,
            text=f"Welcome, {user.full_name}",
            font=("Arial", 16, "bold"),
        ).pack(side="left")

        ttk.Label(header, text=f"Role: {user.role}", font=("Arial", 11)).pack(side="left", padx=12)

        ttk.Button(header, text="Logout", command=self.app.logout_user).pack(side="right")

        body = ttk.LabelFrame(self, text="Actions")
        body.pack(fill="x", pady=4)

        if user.role == ROLE_USER:
            ttk.Button(body, text="New Booking", command=self.app.show_booking_form).pack(
                fill="x", padx=10, pady=8
            )
            ttk.Button(body, text="My Bookings", command=self.app.show_booking_list).pack(
                fill="x", padx=10, pady=8
            )

        if user.role == ROLE_DRIVER:
            ttk.Button(body, text="My Assigned Trips", command=self.app.show_driver_trips).pack(
                fill="x", padx=10, pady=8
            )

        if user.role == ROLE_ADMIN:
            ttk.Button(body, text="Admin Panel", command=self.app.show_admin_panel).pack(
                fill="x", padx=10, pady=(8, 10)
            )

        creds = ttk.LabelFrame(self, text="Default Admin Credentials")
        creds.pack(fill="x", pady=10)
        ttk.Label(
            creds,
            text=(
                "Admin: admin@taxi.local / Admin@123\n"
                "Driver 1: driver1@taxi.local / Driver@123\n"
                "Driver 2: driver2@taxi.local / Driver@123"
            ),
        ).pack(anchor="w", padx=10, pady=10)
