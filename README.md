# Lost & Found WebApp

A modern Flask application that helps our campus community report, find, and reunite lost items—securely and beautifully.

- Contemporary UI with glassmorphism theme and responsive layouts
- Email verification for new accounts (Gmail SMTP supported)
- Phone OTP password reset (Twilio Verify supported, with SMS fallback)
- Report Lost/Found items with optional photos and fast search

## Table of Contents
- Overview
- Features
- System Architecture & Stack
- Folder Structure
- Data Model
- Authentication & Security
- Configuration (.env)
- Local Development
- Database Setup
- How It Works (Routes & Flows)
- File Uploads
- PEP 8 Style & Code Quality
- Testing & Quick Checks
- Deployment
- Team

## Overview
Lost & Found WebApp is tailored for campus use. It offers an intuitive way to report lost or found items, search the catalog, and manage posts from a personal dashboard. The app enforces email verification for new accounts and supports phone OTP for password resets.

## Features
- Beautiful, responsive UI with glassmorphism effects
- Guest landing page with search and an authenticated dashboard
- Authentication flows:
  - Registration (requires phone number)
  - Email verification (must verify before login)
  - Login/logout
  - “Forgot password?” via phone OTP (Twilio Verify preferred)
  - Password eye toggles and confirm-password validation
- Report Lost / Report Found items (optional photo upload)
- Item details view
- Search by keyword, item type, and status
- About page with team info

## System Architecture & Stack
- Backend: Flask 2.x
- ORM: SQLAlchemy
- Auth: Flask-Login
- Email: Flask-Mail (Gmail SMTP supported)
- SMS/OTP: Twilio Verify (preferred) or raw SMS fallback
- Migrations: Flask-Migrate
- Templates: Jinja2 (HTML + CSS + minimalist JS)
- Static: served via Flask; images under `app/static/`

Key modules and files
- `app/__init__.py`: App initialization (Flask, SQLAlchemy, LoginManager, Mail, dotenv)
- `app/models.py`: Data models (`User`, `Item`)
- `app/auth.py`: Auth helpers (password hashing, email/phone verification, OTP)
- `app/routes.py`: All web routes and flows
- `app/templates/`: Pages (base layout, login/register, dashboard, reports, details, verify flows)
- `config.py`: Configuration loaded from environment variables
- `init_db.py`: Quick SQLite table creation utility
- `run.py`: Dev server entry point (port 5001)

## Folder Structure
```
lost-found-WebApp/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── auth.py
│   ├── static/
│   │   └── images/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── report_lost.html
│       ├── report_found.html
│       ├── item_details.html
│       ├── verify_email.html
│       ├── forgot_password.html
│       ├── verify_reset_code.html
│       └── reset_password.html
├── migrations/
├── tests/
├── .env.example
├── requirements.txt
├── config.py
├── init_db.py
├── run.py
├── DEPLOYMENT.md
└── README.md
```

## Data Model
User
- id, name, campus_id (unique), email (unique), phone (unique), department
- password_hash (Werkzeug)
- email_verified (bool), email_verification_code (6-digit string)
- phone_verified (bool), phone_verification_code (6-digit string)

Item
- id, title, description, item_type (lost|found)
- contact_phone, photo_filename (optional)
- date_reported, status (active|resolved), user_id (FK)

## Authentication & Security
- Passwords hashed with Werkzeug; never stored in plaintext.
- Email verification is required before login (`email_verified == True`).
- Phone OTP for password reset:
  - Preferred: Twilio Verify (no local code stored; verification checked via Verify API)
  - Fallback: Local 6-digit code (+ SMS) when Verify is not configured
- SECRET_KEY must be set in production; keep `.env` private and never commit secrets.

## Configuration (.env)
Copy `.env.example` to `.env` and fill with your values.

Basics
- `SECRET_KEY`=change-me
- `DATABASE_URL`=sqlite:///lost_found.db (or a Postgres URL)

Gmail SMTP (email verification)
- `MAIL_SERVER`=smtp.gmail.com
- `MAIL_PORT`=587
- `MAIL_USE_TLS`=True
- `MAIL_USERNAME`=your-email@gmail.com
- `MAIL_PASSWORD`=your-16-char-app-password
- `MAIL_DEFAULT_SENDER`=your-email@gmail.com

Twilio (Phone OTP)
- `TWILIO_ACCOUNT_SID`=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
- `TWILIO_AUTH_TOKEN`=your_auth_token
- `TWILIO_VERIFY_SERVICE_SID`=VAxxxxxxxxxxxxxxxxxxxxxxxx (preferred)
- `TWILIO_PHONE_NUMBER`=+12025550123 (optional; used for fallback non-Verify SMS)

Notes
- We load `.env` automatically in development (`python-dotenv`).
- Twilio Verify requires E.164 phone numbers (e.g., +2330551493205).
- Gmail requires enabling 2FA and creating an App Password.

## Local Development
Prerequisites: Python 3.10+

```bash
git clone <repo-url>
cd lost-found-WebApp

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env to set SECRET_KEY, MAIL_*, and TWILIO_* as needed

# Option A: Quick DB create (SQLite)
python init_db.py

# Option B: Using migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run app (dev)
python run.py
```

By default, the app runs on http://127.0.0.1:5001

## Database Setup
Two options are available:
1) Quick start with `init_db.py` (creates tables using `db.create_all()`)
2) Full migration flow with Flask-Migrate (recommended for teams/production)

## How It Works (Routes & Flows)
Public routes
- `/` Landing page (search for items)
- `/about` About & team
- `/login` Sign in (password eye toggle)
- `/register` Sign up (requires phone; confirm password + eye toggles)
- `/verify-email` Submit email + 6-digit code to verify
- `/resend-email-code` POST to resend verification email
- `/forgot-password` Start phone OTP reset (enter phone, E.164 format)
- `/verify-reset-code` Verify 6-digit phone code
- `/reset-password` Set a new password

Authenticated (email verified) routes
- `/dashboard` Recent items
- `/report_lost` Report a lost item (photo optional)
- `/report_found` Report a found item (photo optional)
- `/item/<id>` Item details
- `/search` Search with filters (type, status, query)

## File Uploads
- Allowed: `png, jpg, jpeg, gif`
- Max size: 5 MB
- Stored at `app/static/uploads/` with UUID filenames

## PEP 8 Style & Code Quality
- Follow PEP 8 (4-space indentation; sensible line lengths ~88–100)
- Naming: `snake_case` for functions/variables; `PascalCase` for classes
- Imports grouped: stdlib, third-party, local

Suggested tools (optional)
```bash
pip install black flake8 isort
black app/ init_db.py
flake8 app/
isort app/
```

## Testing & Quick Checks
Manual sanity checks
- Register: requires phone → redirected to Verify Email → verify code → login works
- Password reset: Forgot password → phone OTP → verify → set new password
- Items: Report Lost/Found with/without photo → dashboard and details show it → search works

Automated tests
- `tests/` scaffold is present—extend with pytest or unittest as needed.

## Deployment
See `DEPLOYMENT.md` for platform-specific steps (Render, Railway, Heroku, etc.).
- Set production env vars: SECRET_KEY, DATABASE_URL, MAIL_*, TWILIO_*
- Example start command: `gunicorn run:app`

## Team
- Nicholas Dornyo
- Daniel Eli Dumedah
- Daniel Nana Kojo Adjei
- Nhyiraba Agyeman Peprah
- Kingsley

— Level 100 Computer Science Students, Accra Technical University
