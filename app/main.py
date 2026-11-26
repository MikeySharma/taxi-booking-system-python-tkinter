from __future__ import annotations

from app.db.connection import get_db
from app.db.seed import seed_admin, seed_sample_data
from app.ui.app_window import AppWindow


def main() -> None:
    db = get_db()
    db.init_schema()
    seed_admin(db)
    seed_sample_data(db)

    app = AppWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
