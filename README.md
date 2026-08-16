# AgriRental — Agricultural Equipment Rental System

A production-structured Flask application connecting farmers with equipment
owners (tractors, harvesters, tillers, ploughs, sprayers, drones) for
day-rate rentals.

## Project structure

```
agri_rental_system/
├── app/
│   ├── __init__.py              # App factory (create_app)
│   ├── config.py                # Dev / Prod / Testing config classes
│   ├── extensions.py            # db, login_manager, bcrypt, jwt, migrate, cors
│   │
│   ├── models/                  # SQLAlchemy models (one file per entity)
│   │   ├── user.py              # User + UserRole (farmer / owner / admin)
│   │   ├── equipment.py         # Equipment + EquipmentCategory
│   │   ├── booking.py           # Booking + BookingStatus
│   │   ├── payment.py           # Payment + PaymentStatus (mock gateway)
│   │   └── review.py            # Review / rating
│   │
│   ├── routes/                  # Blueprints (controllers)
│   │   ├── auth.py              # register / login / logout
│   │   ├── main.py              # home + role-aware dashboard
│   │   ├── equipment.py         # listing, detail, create (owner only)
│   │   └── booking.py           # create booking + mock payment
│   │
│   ├── utils/
│   │   ├── decorators.py        # @role_required, @admin_required
│   │   └── validators.py        # image upload validation
│   │
│   ├── templates/
│   │   ├── base.html            # layout shell, navbar, flash messages
│   │   ├── index.html           # landing page
│   │   ├── auth/
│   │   │   ├── login.html       # ★ animated sunrise-field login (see below)
│   │   │   └── register.html
│   │   ├── equipment/
│   │   │   ├── list.html        # filterable marketplace grid
│   │   │   ├── detail.html      # equipment page + booking form
│   │   │   └── form.html        # owner: list new equipment
│   │   ├── dashboard/
│   │   │   ├── farmer.html
│   │   │   ├── owner.html
│   │   │   └── admin.html
│   │   ├── partials/
│   │   │   ├── navbar.html / footer.html
│   │   │   └── equipment_icons.html   # inline SVG equipment art (by category)
│   │   └── errors/               # 404 / 403
│   │
│   └── static/
│       ├── css/style.css         # design-token system (see below)
│       ├── js/
│       └── img/equipment/        # uploaded equipment photos land here
│
├── migrations/                   # created by `flask db init`
├── tests/                        # pytest test package
├── instance/                     # local SQLite db lives here (gitignored)
├── seed.py                       # demo users + equipment for local testing
├── run.py                        # entry point (`python run.py`)
├── requirements.txt
└── .env.example
```

## Design: the login page

The login/register screens are the deliberately "lively" piece of the
app — a split-screen layout: an animated sunrise-over-the-field scene
(SVG sun rising, a tractor driving across on a loop, drifting birds) on
the left, and a clean cream-and-green form card on the right. All colors
are CSS custom properties in `static/css/style.css` (`--soil-900`,
`--crop-600`, `--sun-500`, `--sky-400`, `--cream-50`) so the palette is
consistent across the whole app, not just the login page.

## Equipment "images"

Two image sources are supported:
1. **Uploaded photos** — owners upload a real photo when listing
   equipment (`equipment/form.html`), stored under
   `static/img/equipment/` with a UUID filename (see
   `utils/validators.py::save_equipment_image`).
2. **Category illustrations** — until a photo is uploaded, each
   equipment card falls back to a hand-drawn inline SVG matching its
   category (tractor, harvester, tiller, plough, sprayer, drone,
   irrigation) from `partials/equipment_icons.html`. This keeps the
   marketplace visually complete from day one and avoids relying on
   external/copyrighted stock photos.

## Setup

```bash
cd agri_rental_system
python -m venv venv && source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                 # then edit secrets

# initialize the database
flask db init && flask db migrate -m "initial" && flask db upgrade
# (or, for a quick local run without migrations:)
python seed.py                                        # creates tables + demo data

python run.py                                          # http://localhost:5000
```

Demo logins after `python seed.py`:
- Owner:  `owner@example.com`  / `password123`
- Farmer: `farmer@example.com` / `password123`

## Key architectural choices

- **App factory pattern** (`create_app`) + blueprints — keeps the app
  testable and avoids circular imports.
- **Role-based access** — `User.role` is `farmer` / `owner` / `admin`;
  `@role_required(...)` decorator gates owner-only routes like listing
  equipment.
- **Mock payment gateway** in `routes/booking.py` — swap the block that
  creates the `Payment` row with a real Razorpay/Stripe order + webhook
  without touching the booking logic.
- **Config classes** per environment (`DevelopmentConfig`,
  `ProductionConfig`, `TestingConfig`) selected via `FLASK_ENV`.

## Suggested next steps

- Add `Flask-WTF` forms with server-side validation messages per field.
- Add equipment availability calendar (block out already-booked dates).
- Add real payment gateway integration (Razorpay is common for India).
- Add owner equipment edit/delete + booking cancellation flows.
- Write pytest coverage in `tests/` for auth and booking flows.
