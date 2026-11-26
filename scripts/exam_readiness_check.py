from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _check_exists(relative_path: str) -> tuple[bool, str]:
    target = ROOT / relative_path
    return target.exists(), f"{relative_path} {'found' if target.exists() else 'missing'}"


def _check_text_contains(relative_path: str, needles: list[str]) -> tuple[bool, str]:
    target = ROOT / relative_path
    if not target.exists():
        return False, f"{relative_path} missing"
    text = target.read_text(encoding="utf-8")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, f"{relative_path} missing: {', '.join(missing)}"
    return True, f"{relative_path} contains required items"


def _run_tests() -> tuple[bool, str]:
    cmd = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
    process = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    output_path = ROOT / "report_evidence" / "testing" / "unit-test-output.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined = process.stdout + "\n" + process.stderr
    output_path.write_text(combined.strip() + "\n", encoding="utf-8")

    if process.returncode == 0:
        return True, f"Tests passed. Output saved to {output_path.relative_to(ROOT)}"
    return False, f"Tests failed. See {output_path.relative_to(ROOT)}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Project exam-readiness checklist")
    parser.add_argument(
        "--run-tests",
        action="store_true",
        help="Run unit tests and save output to report_evidence/testing/unit-test-output.txt",
    )
    args = parser.parse_args()

    checks: list[tuple[str, bool, str]] = []

    required_paths = [
        "app/main.py",
        "app/ui/admin_view.py",
        "app/ui/driver_trips_view.py",
        "app/services/booking_service.py",
        "app/db/schema.sql",
        "tests/test_booking_service.py",
        "report_evidence/README.md",
        "report_evidence/testing/test-cases-template.md",
    ]
    for rel in required_paths:
        ok, detail = _check_exists(rel)
        checks.append((f"Required file: {rel}", ok, detail))

    ok, detail = _check_text_contains(
        "app/utils/constants.py",
        ["ROLE_USER", "ROLE_DRIVER", "ROLE_ADMIN"],
    )
    checks.append(("Roles configured", ok, detail))

    ok, detail = _check_text_contains(
        "app/db/schema.sql",
        ["address", "scheduled_date", "scheduled_time", "assigned_driver_id"],
    )
    checks.append(("Schema includes required fields", ok, detail))

    ok, detail = _check_text_contains(
        "app/services/booking_service.py",
        ["assign_driver", "has_driver_overlap", "get_driver_bookings"],
    )
    checks.append(("Driver assignment logic exists", ok, detail))

    if args.run_tests:
        ok, detail = _run_tests()
        checks.append(("Unit tests", ok, detail))

    print("Exam Readiness Checklist\n")
    failures = 0
    for title, ok, detail in checks:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {title}")
        print(f"       {detail}")
        if not ok:
            failures += 1

    print("\nManual checks before submission:")
    print("- Capture screenshots in report_evidence/screenshots/*")
    print("- Fill test tables in report_evidence/testing/test-cases-template.md")
    print("- Fill execution notes in report_evidence/testing/test-execution-log.md")
    print("- Verify report + diagrams + video are complete")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
