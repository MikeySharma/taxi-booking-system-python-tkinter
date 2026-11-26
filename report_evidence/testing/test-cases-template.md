# Test Cases Template

Use this table for your report testing section.

| TC ID | Module | Scenario | Input Data | Expected Result | Actual Result | Status (Pass/Fail) | Evidence (screenshot path) |
|------:|--------|----------|------------|-----------------|---------------|--------------------|----------------------------|
| TC-01 | Auth | Customer registration success | Valid name/address/phone/email/password | Account is created and login possible |  |  | `screenshots/01-login-register/...` |
| TC-02 | Auth | Registration validation failure | Missing address | Validation message shown |  |  | `screenshots/05-validation-errors/...` |
| TC-03 | Auth | Login failure | Wrong password | Login denied with error |  |  | `screenshots/05-validation-errors/...` |
| TC-04 | Customer Booking | Create booking success | Valid pickup/drop/date/time/distance/car | Booking created and shown in list |  |  | `screenshots/02-customer-booking/...` |
| TC-05 | Customer Booking | Edit pending booking | Updated date/time/dropoff | Booking details updated |  |  | `screenshots/02-customer-booking/...` |
| TC-06 | Customer Booking | Cancel pending booking | Select pending booking + cancel | Status becomes cancelled |  |  | `screenshots/02-customer-booking/...` |
| TC-07 | Admin | Assign driver success | Booking A + Driver 1 | Driver assigned |  |  | `screenshots/03-admin-driver-assignment/...` |
| TC-08 | Admin | Prevent overlap | Booking B same slot + Driver 1 | Overlap error shown |  |  | `screenshots/03-admin-driver-assignment/...` |
| TC-09 | Driver | View assigned trips | Login as driver | Assigned trips list displayed |  |  | `screenshots/04-driver-trips/...` |
| TC-10 | Admin | Update booking status | Select booking + status | Status updated |  |  | `screenshots/03-admin-driver-assignment/...` |
