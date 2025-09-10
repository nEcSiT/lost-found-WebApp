from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import login_manager, db

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

def register_user(name, campus_id, email, password):
	password_hash = generate_password_hash(password)
	user = User(name=name, campus_id=campus_id, email=email, password_hash=password_hash)
	db.session.add(user)
	db.session.commit()
	return user

def verify_user(email, password):
	user = User.query.filter_by(email=email).first()
	if user and check_password_hash(user.password_hash, password):
		return user
	return None
