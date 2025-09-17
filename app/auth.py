from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import login_manager, db, mail, app
from flask_mail import Message
import random
import os
try:
	from twilio.rest import Client  # optional; we won't use if verification disabled
except Exception:
	Client = None

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

def generate_verification_code():
	return str(random.randint(100000, 999999))

def send_email_verification(email, code):
	# Email verification disabled: no-op (log in dev)
	print(f"[DEV MODE] Email verification code for {email}: {code}")

def send_sms_verification(phone, code):
	# Twilio disabled: just print the code for dev/local use
	print(f"[DEV MODE] SMS verification code for {phone}: {code}")

def register_user(name, campus_id, email, password, department, phone):
	from sqlalchemy.exc import IntegrityError
	
	# Validate required fields
	if not phone:
		raise ValueError("Phone number is required")
	
	# Check if user already exists
	existing_user_email = User.query.filter_by(email=email).first()
	if existing_user_email:
		raise ValueError("Email address is already registered")
	
	existing_user_campus = User.query.filter_by(campus_id=campus_id).first()
	if existing_user_campus:
		raise ValueError("Campus ID is already registered")
	
	existing_user_phone = User.query.filter_by(phone=phone).first()
	if existing_user_phone:
		raise ValueError("Phone number is already registered")
	
	password_hash = generate_password_hash(password)
	# Disable verification for now: no codes needed
	email_code = None
	phone_code = None
    
	# Default now: auto-verify (no email/phone verification required)
	user = User(
		name=name,
		campus_id=campus_id,
		email=email,
		department=department,
		password_hash=password_hash,
		phone=phone,
		email_verification_code=email_code,
		phone_verification_code=phone_code,
		email_verified=True,
		phone_verified=True,
	)
	try:
		db.session.add(user)
		db.session.commit()

		# Verification disabled: do not send email/SMS codes
		return user
	except IntegrityError as e:
		db.session.rollback()
		if 'user.email' in str(e):
			raise ValueError("Email address is already registered")
		elif 'user.campus_id' in str(e):
			raise ValueError("Campus ID is already registered")
		elif 'user.phone' in str(e):
			raise ValueError("Phone number is already registered")
		else:
			raise ValueError("Registration failed due to duplicate information")

def verify_user(campus_id, password):
	user = User.query.filter_by(campus_id=campus_id).first()
	if user and check_password_hash(user.password_hash, password):
		return user
	return None


def verify_email_code(email: str, code: str) -> bool:
	"""Email verification disabled: always return True if user exists."""
	user = User.query.filter_by(email=email).first()
	return bool(user)


def resend_email_code(email: str) -> bool:
	# Disabled: pretend to resend successfully if user exists
	user = User.query.filter_by(email=email).first()
	return bool(user)


def generate_phone_reset_code(phone: str) -> bool:
	"""Generate and send a phone OTP for password reset.

	If Twilio Verify is configured, trigger a Verify SMS and don't store a code locally.
	Otherwise, generate/store a code and send via SMS or dev print.
	"""
	user = User.query.filter_by(phone=phone).first()
	if not user:
		return False

	# Twilio disabled: always use local code path
	code = generate_verification_code()
	user.phone_verification_code = code
	db.session.commit()
	send_sms_verification(phone, code)
	return True


def verify_phone_code(phone: str, code: str) -> User | None:
	"""Verify a phone code; with Twilio Verify, check remotely; otherwise, compare stored code."""
	user = User.query.filter_by(phone=phone).first()
	if not user:
		return None

	# Local code path only (Twilio disabled)
	if user.phone_verification_code and user.phone_verification_code == code:
		return user
	return None


def update_user_password(user: User, new_password: str) -> None:
	user.password_hash = generate_password_hash(new_password)
	# clear the phone code once used
	user.phone_verification_code = None
	db.session.commit()
