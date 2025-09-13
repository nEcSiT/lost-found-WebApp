from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	campus_id = db.Column(db.String(50), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	phone = db.Column(db.String(20), unique=True, nullable=False)
	department = db.Column(db.String(100), nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)
	email_verified = db.Column(db.Boolean, default=False)
	email_verification_code = db.Column(db.String(6))
	phone_verified = db.Column(db.Boolean, default=False)
	phone_verification_code = db.Column(db.String(6))
	items = db.relationship('Item', backref='user', lazy=True)

class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	description = db.Column(db.Text, nullable=False)
	item_type = db.Column(db.String(10), nullable=False)  # 'lost' or 'found'
	contact_phone = db.Column(db.String(20), nullable=False)  # Contact phone for this item
	photo_filename = db.Column(db.String(255))  # Optional photo filename
	date_reported = db.Column(db.DateTime, nullable=False)
	status = db.Column(db.String(20), default='active')  # 'active', 'resolved', etc.
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
