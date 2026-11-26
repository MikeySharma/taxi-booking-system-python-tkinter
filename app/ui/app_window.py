from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from app.config import APP_GEOMETRY, APP_TITLE
from app.db.connection import get_db
from app.repositories.booking_repository import BookingRepository
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.booking_service import BookingService
from app.services.fare_service import FareService


class AppWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)
        self.minsize(960, 640)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.current_user = None
        self.current_frame: ttk.Frame | None = None

        self.db = get_db()
        self.user_repo = UserRepository(self.db)
        self.booking_repo = BookingRepository(self.db)
        self.auth_service = AuthService(self.user_repo)
        self.fare_service = FareService()
        self.booking_service = BookingService(self.booking_repo, self.fare_service, self.user_repo)

        self.show_login()

    def _show_frame(self, frame_cls):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = frame_cls(self)
        self.current_frame.pack(fill="both", expand=True, padx=16, pady=16)

    def show_login(self):
        from app.ui.login_view import LoginView

        self._show_frame(LoginView)

    def show_register(self):
        from app.ui.register_view import RegisterView

        self._show_frame(RegisterView)

    def show_dashboard(self):
        from app.ui.dashboard_view import DashboardView

        self._show_frame(DashboardView)

    def show_booking_form(self):
        from app.ui.booking_form_view import BookingFormView

        self._show_frame(BookingFormView)

    def show_booking_list(self):
        from app.ui.booking_list_view import BookingListView

        self._show_frame(BookingListView)

    def show_admin_panel(self):
        from app.ui.admin_view import AdminView

        self._show_frame(AdminView)

    def show_driver_trips(self):
        from app.ui.driver_trips_view import DriverTripsView

        self._show_frame(DriverTripsView)

    def login_user(self, user):
        self.current_user = user
        self.show_dashboard()

    def logout_user(self):
        self.current_user = None
        self.show_login()
