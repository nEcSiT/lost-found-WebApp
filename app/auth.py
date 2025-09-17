from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import login_manager, db, mail, app
from flask_mail import Message
import random
import os
from twilio.rest import Client

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

def generate_verification_code():
	return str(random.randint(100000, 999999))

def send_email_verification(email, code):
	try:
		if app.config.get('MAIL_SERVER') and app.config.get('MAIL_USERNAME') and app.config.get('MAIL_PASSWORD'):
			sender = app.config.get('MAIL_DEFAULT_SENDER') or app.config.get('MAIL_USERNAME')
			msg = Message('Your Email Verification Code', recipients=[email], sender=sender)
			msg.body = f'Your verification code is: {code}'
			mail.send(msg)
			print(f"[MAIL SENT] Verification code sent to {email}")
		else:
			print(f"[DEV MODE] Email verification code for {email}: {code}")
	except Exception as e:
		print(f"[MAIL ERROR] {str(e)}")
		print(f"[DEV MODE] Email verification code for {email}: {code}")

def send_sms_verification(phone, code):
	try:
		# Prefer Twilio Verify if configured
		account_sid = app.config.get('TWILIO_ACCOUNT_SID') or os.environ.get('TWILIO_ACCOUNT_SID')
		auth_token = app.config.get('TWILIO_AUTH_TOKEN') or os.environ.get('TWILIO_AUTH_TOKEN')
		verify_service_sid = app.config.get('TWILIO_VERIFY_SERVICE_SID') or os.environ.get('TWILIO_VERIFY_SERVICE_SID')
		twilio_number = app.config.get('TWILIO_PHONE_NUMBER') or os.environ.get('TWILIO_PHONE_NUMBER')
		
		client = None
		if account_sid and auth_token:
			client = Client(account_sid, auth_token)

		if client and verify_service_sid:
			# Use Verify service to send a verification code
			client.verify.v2.services(verify_service_sid).verifications.create(to=phone, channel='sms')
			print(f"[VERIFY SENT] Verification code sent via Twilio Verify to {phone}")
		elif client and twilio_number:
			# Fallback: send raw SMS if Verify service isn't configured
			client.messages.create(
				body=f'Your Campus Lost & Found verification code is: {code}',
				from_=twilio_number,
				to=phone
			)
			print(f"[SMS SENT] Verification code sent to {phone}")
		else:
			# Fallback for development when Twilio is not configured
			print(f"[DEV MODE] SMS verification code for {phone}: {code}")
	except Exception as e:
		# Fallback to development mode if Twilio fails
		print(f"[DEV MODE] SMS verification code for {phone}: {code}")
		print(f"[SMS ERROR] {str(e)}")

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
	email_code = generate_verification_code()
	phone_code = generate_verification_code()
    
	# Default: require verification (dev prints codes to console)
	user = User(
		name=name,
		campus_id=campus_id,
		email=email,
		department=department,
		password_hash=password_hash,
		phone=phone,
		email_verification_code=email_code,
		phone_verification_code=phone_code,
		email_verified=False,
		phone_verified=False,
	)
	
	try:
		db.session.add(user)
		db.session.commit()
		
	# Send verification codes (development mode will print to console)
		send_email_verification(email, email_code)
		send_sms_verification(phone, phone_code)
		
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
	"""Verify a user's email with a 6-digit code."""
	user = User.query.filter_by(email=email).first()
	if not user:
		return False
	if user.email_verified:
		return True
	if user.email_verification_code and user.email_verification_code == code:
		user.email_verified = True
		user.email_verification_code = None
		db.session.commit()
		return True
	return False


def resend_email_code(email: str) -> bool:
	user = User.query.filter_by(email=email).first()
	if not user:
		return False
	# generate new code and send
	code = generate_verification_code()
	user.email_verification_code = code
	db.session.commit()
	send_email_verification(email, code)
	return True


def generate_phone_reset_code(phone: str) -> bool:
	"""Generate and send a phone OTP for password reset.

	If Twilio Verify is configured, trigger a Verify SMS and don't store a code locally.
	Otherwise, generate/store a code and send via SMS or dev print.
	"""
	user = User.query.filter_by(phone=phone).first()
	if not user:
		return False

	verify_service_sid = app.config.get('TWILIO_VERIFY_SERVICE_SID') or os.environ.get('TWILIO_VERIFY_SERVICE_SID')
	account_sid = app.config.get('TWILIO_ACCOUNT_SID') or os.environ.get('TWILIO_ACCOUNT_SID')
	auth_token = app.config.get('TWILIO_AUTH_TOKEN') or os.environ.get('TWILIO_AUTH_TOKEN')

	if verify_service_sid and account_sid and auth_token:
		try:
			client = Client(account_sid, auth_token)
			client.verify.v2.services(verify_service_sid).verifications.create(to=phone, channel='sms')
			# No local code needed with Verify
			print(f"[VERIFY SENT] Password reset code sent via Twilio Verify to {phone}")
			return True
		except Exception as e:
			print(f"[VERIFY ERROR] {e}")
			# Fall through to local code path

	# Local code path (no Verify)
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

	verify_service_sid = app.config.get('TWILIO_VERIFY_SERVICE_SID') or os.environ.get('TWILIO_VERIFY_SERVICE_SID')
	account_sid = app.config.get('TWILIO_ACCOUNT_SID') or os.environ.get('TWILIO_ACCOUNT_SID')
	auth_token = app.config.get('TWILIO_AUTH_TOKEN') or os.environ.get('TWILIO_AUTH_TOKEN')

	if verify_service_sid and account_sid and auth_token:
		try:
			client = Client(account_sid, auth_token)
			verification_check = client.verify.v2.services(verify_service_sid).verification_checks.create(to=phone, code=code)
			if verification_check.status == 'approved':
				return user
			return None
		except Exception as e:
			print(f"[VERIFY CHECK ERROR] {e}")
			return None

	# Local code path
	if user.phone_verification_code and user.phone_verification_code == code:
		return user
	return None


def update_user_password(user: User, new_password: str) -> None:
	user.password_hash = generate_password_hash(new_password)
	# clear the phone code once used
	user.phone_verification_code = None
	db.session.commit()
