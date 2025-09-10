# Lost & Found WebApp

## Overview
This is a campus lost and found web application built with Flask (Python), SQLAlchemy, Flask-Login, HTML, CSS, and JavaScript. It allows users to report, search, and manage lost and found items securely.

## Features
- User registration and login (authentication)
- Report lost or found items
- View recent uploads
- Search for items
- Dashboard for logged-in users
- Database migrations with Flask-Migrate

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
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── dashboard.html
│       ├── report_lost.html
│       └── report_found.html
├── migrations/
├── tests/
├── .env
├── requirements.txt
├── config.py
├── run.py
└── README.md
```

## Setup Instructions
1. **Clone the repository**
	```bash
	git clone <repo-url>
	cd lost-found-WebApp
	```
2. **Create and activate a virtual environment**
	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	```
3. **Install dependencies**
	```bash
	pip install -r requirements.txt
	```
4. **Set up environment variables**
	- Edit `.env` with your secret key and database URL if needed.
5. **Initialize the database**
	```bash
	flask db init
	flask db migrate -m "Initial migration"
	flask db upgrade
	```
6. **Run the app**
	```bash
	.venv/bin/python run.py
	```

## Usage
- Register a new account or log in.
- Use the dashboard to report lost/found items, search, and view recent uploads.
- Log out when done.

## Contributing
1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes and commit
4. Submit a pull request

## License
This project is licensed under the MIT License.
