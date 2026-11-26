from __future__ import annotations

from tkinter import messagebox
from tkinter import ttk


class LoginView(ttk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        container = ttk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(container, text="Taxi Booking System", font=("Arial", 20, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 16)
        )
        ttk.Label(container, text="Login", font=("Arial", 14)).grid(
            row=1, column=0, columnspan=2, pady=(0, 16)
        )

        ttk.Label(container, text="Email").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=6)
        self.email_entry = ttk.Entry(container, width=36)
        self.email_entry.grid(row=2, column=1, pady=6)

        ttk.Label(container, text="Password").grid(
            row=3, column=0, sticky="w", padx=(0, 8), pady=6
        )
        self.password_entry = ttk.Entry(container, width=36, show="*")
        self.password_entry.grid(row=3, column=1, pady=6)

        ttk.Button(container, text="Login", command=self.on_login).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=(12, 6)
        )
        ttk.Button(container, text="Create account", command=self.app.show_register).grid(
            row=5, column=0, columnspan=2, sticky="ew"
        )

    def on_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        ok, message, user = self.app.auth_service.login(email, password)
        if not ok or user is None:
            messagebox.showerror("Login failed", message)
            return

        messagebox.showinfo("Login", f"Welcome, {user.full_name}!")
        self.app.login_user(user)
