from __future__ import annotations

from tkinter import messagebox
from tkinter import ttk


class RegisterView(ttk.Frame):
    def __init__(self, app):
        super().__init__(app)
        self.app = app

        container = ttk.Frame(self)
        container.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(container, text="Create Account", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 16)
        )

        ttk.Label(container, text="Full name").grid(row=1, column=0, sticky="w", pady=5, padx=(0, 8))
        self.full_name_entry = ttk.Entry(container, width=36)
        self.full_name_entry.grid(row=1, column=1, pady=5)

        ttk.Label(container, text="Address").grid(row=2, column=0, sticky="w", pady=5, padx=(0, 8))
        self.address_entry = ttk.Entry(container, width=36)
        self.address_entry.grid(row=2, column=1, pady=5)

        ttk.Label(container, text="Phone").grid(row=3, column=0, sticky="w", pady=5, padx=(0, 8))
        self.phone_entry = ttk.Entry(container, width=36)
        self.phone_entry.grid(row=3, column=1, pady=5)

        ttk.Label(container, text="Email").grid(row=4, column=0, sticky="w", pady=5, padx=(0, 8))
        self.email_entry = ttk.Entry(container, width=36)
        self.email_entry.grid(row=4, column=1, pady=5)

        ttk.Label(container, text="Password").grid(row=5, column=0, sticky="w", pady=5, padx=(0, 8))
        self.password_entry = ttk.Entry(container, width=36, show="*")
        self.password_entry.grid(row=5, column=1, pady=5)

        ttk.Label(container, text="Confirm password").grid(
            row=6, column=0, sticky="w", pady=5, padx=(0, 8)
        )
        self.confirm_entry = ttk.Entry(container, width=36, show="*")
        self.confirm_entry.grid(row=6, column=1, pady=5)

        ttk.Button(container, text="Register", command=self.on_register).grid(
            row=7, column=0, columnspan=2, sticky="ew", pady=(12, 6)
        )
        ttk.Button(container, text="Back to login", command=self.app.show_login).grid(
            row=8, column=0, columnspan=2, sticky="ew"
        )

    def on_register(self):
        ok, message, user = self.app.auth_service.register(
            full_name=self.full_name_entry.get(),
            address=self.address_entry.get(),
            phone=self.phone_entry.get(),
            email=self.email_entry.get(),
            password=self.password_entry.get(),
            confirm_password=self.confirm_entry.get(),
        )
        if not ok or user is None:
            messagebox.showerror("Registration failed", message)
            return

        messagebox.showinfo("Registration", "Account created successfully. Please login.")
        self.app.show_login()
