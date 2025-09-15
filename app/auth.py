from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import login_manager, db, mail
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
	# For development: Skip actual email sending
	# In production, you would configure a proper email service
	print(f"[DEV MODE] Email verification code for {email}: {code}")
	# Uncomment below when email server is configured
	# msg = Message('Your Email Verification Code', recipients=[email])
	# msg.body = f'Your verification code is: {code}'
	# mail.send(msg)

def send_sms_verification(phone, code):
	try:
		# Try to send via Twilio if configured
		account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
		auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
		twilio_number = os.environ.get('TWILIO_PHONE_NUMBER')
		
		if account_sid and auth_token and twilio_number:
			client = Client(account_sid, auth_token)
			message = client.messages.create(
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
	
	# For development: Auto-verify users
	user = User(name=name, campus_id=campus_id, email=email, department=department, password_hash=password_hash,
				phone=phone, email_verification_code=email_code, phone_verification_code=phone_code,
				email_verified=True, phone_verified=True)
	
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
