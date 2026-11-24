# TrekZon 🧭

A trek booking and management system built with Flask. TrekZon exists to take the chaos out of running a trekking business — admins get a control room, staff get a way to run their assigned trips without digging through spreadsheets, and trekkers get a simple place to find and reserve a spot on their next climb.

`Python 3.8+` · `Flask 3.0` · `SQLite`

---

## Why this exists

Small trekking outfits usually juggle bookings across WhatsApp, Excel, and memory. TrekZon replaces that with one shared system where every role sees exactly what it needs and nothing more.

---

## Who uses it

**Admin** — owns the whole system. Creates and retires treks, onboards staff, freezes or restores accounts, and can see every booking across the organization at once.

**Trek Staff** — sees only the treks they've been put in charge of. Can flip a trek's status between Open, Ongoing, and Completed, and pull up the list of everyone signed up for a given expedition.

**Trekker** — the end customer. Browses open treks (filterable by destination and difficulty), reserves a slot in one click, and can look back at a personal log of past expeditions once they're done. Can also back out of a booking before it starts.

---

## Under the hood

| Layer | Choice | Why |
|---|---|---|
| Web framework | Flask | Minimal, gives full control over routing/blueprints |
| ORM | Flask-SQLAlchemy | Keeps DB access in Python, no raw SQL scattered around |
| Auth | Werkzeug password hashing | Never store plaintext passwords |
| Templates | Jinja2 | Server-rendered, no separate frontend build step |
| Styling | Bootstrap 5 | Fast to make responsive without writing custom CSS from scratch |
| Charts | Chart.js | Powers the admin stats view |
| Storage | SQLite | Zero-config, fine for a single-instance dev/demo setup |

---

## Data model

Three core tables drive everything:

- **User** — one table, one `role` column (`admin` / `staff` / `trekker`). Keeps auth logic in a single place instead of three separate user tables.
- **Trek** — owned by exactly one staff member (`led_by` FK), has a fixed `slots_total`, and tracks its own lifecycle status.
- **Booking** — the join between a trekker and a trek, carries its own status (`confirmed` / `cancelled`) and a timestamp.

```
User ───────────────< Trek        (one staff leads many treks)
  │
  └──────────────────< Booking >──────────────── Trek
        (one trekker makes many bookings, each tied to one trek)
```

Slot availability is derived at request time: `slots_total - count(active bookings for that trek)`. No separate "slots remaining" counter to keep in sync.

---

## Routes

**Public / auth**
```
GET,POST  /login
GET,POST  /signup
GET       /logout
```

**Admin** (prefix `/admin`)
```
GET        /admin/overview          → stats + charts
GET,POST   /admin/trek/create
GET,POST   /admin/trek/<id>/edit
POST       /admin/trek/<id>/delete
GET,POST   /admin/staff/create
POST       /admin/account/<id>/toggle-status
GET        /admin/bookings/all
```

**Staff** (prefix `/staff`)
```
GET        /staff/overview
GET,POST   /staff/trek/<id>/manage
```

**Trekker** (prefix `/trekker`)
```
GET        /trekker/overview
GET        /trekker/browse
GET        /trekker/trek/<id>
POST       /trekker/trek/<id>/reserve
GET        /trekker/past-treks
```

**Public API**
```
GET  /api/v1/treks
GET  /api/v1/treks/<id>
GET  /api/v1/users/<id>
GET  /api/v1/bookings/<id>
```

---

## Repo layout

```
TrekZon/
├── app.py               entry point, app factory
├── models.py             User / Trek / Booking definitions
├── config.py             env-driven config
├── utils.py               shared helper functions
├── seed_data.py            dev-only fixture generator (not for prod)
├── blueprints/
│   ├── auth.py
│   ├── admin.py
│   ├── staff.py
│   ├── trekker.py
│   └── api.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── auth/  admin/  staff/  trekker/
├── static/css/style.css
└── instance/               sqlite file lives here, gitignored
```

---

## Running it locally

```bash
git clone <repo-url>
cd TrekZon

python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows

pip install -r requirements.txt

python seed_data.py           # optional: populate sample treks/users
python app.py                 # serves on http://127.0.0.1:5000
```

`seed_data.py` is a dev/demo convenience only — it's excluded from anything meant for production.

---

## Try it out

After seeding, these accounts are ready to go:

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `TrekZon@Admin1` |
| Staff | (auto-generated, e.g. `staff_kavya_2`) | `staffPass!2026` |
| Trekker | (auto-generated, e.g. `trekker_ishaan_3`) | `trekPass!2026` |

---

## Status

Actively being built as part of Modern Application Development I. Core milestones (models → auth → dashboards → booking history) are being tracked separately.

---

<div align="center">

Made with ❤️ by **Shaksham Aeron**

</div>
