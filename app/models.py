from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	campus_id = db.Column(db.String(50), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)
	items = db.relationship('Item', backref='user', lazy=True)

class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	description = db.Column(db.Text, nullable=False)
	item_type = db.Column(db.String(10), nullable=False)  # 'lost' or 'found'
	date_reported = db.Column(db.DateTime, nullable=False)
	status = db.Column(db.String(20), default='active')  # 'active', 'resolved', etc.
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
