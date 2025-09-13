from flask import Blueprint, request, jsonify
from .models import User, Item
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

api = Blueprint('api', __name__)
@api.route('/api/verify_email', methods=['POST'])
def api_verify_email():
    data = request.get_json()
    email = data.get('email')
    code = data.get('code')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if user.email_verification_code == code:
        user.email_verified = True
        user.email_verification_code = None
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({'error': 'Database error'}), 500
        return jsonify({'message': 'Email verified successfully'})
    return jsonify({'error': 'Invalid verification code'}), 400

@api.route('/api/verify_phone', methods=['POST'])
def api_verify_phone():
    data = request.get_json()
    phone = data.get('phone')
    code = data.get('code')
    user = User.query.filter_by(phone=phone).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if user.phone_verification_code == code:
        user.phone_verified = True
        user.phone_verification_code = None
        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({'error': 'Database error'}), 500
        return jsonify({'message': 'Phone number verified successfully'})
    return jsonify({'error': 'Invalid verification code'}), 400

@api.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    name = data.get('name')
    campus_id = data.get('campus_id')
    email = data.get('email')
    password = data.get('password')
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    password_hash = generate_password_hash(password)
    user = User(name=name, campus_id=campus_id, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'})

@api.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Login successful', 'user_id': user.id})
    return jsonify({'error': 'Invalid credentials'}), 401

@api.route('/api/items', methods=['GET'])
def api_get_items():
    items = Item.query.order_by(Item.date_reported.desc()).all()
    return jsonify([{
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'item_type': item.item_type,
        'date_reported': item.date_reported.strftime('%Y-%m-%d %H:%M:%S'),
        'status': item.status,
        'user_id': item.user_id
    } for item in items])

@api.route('/api/report', methods=['POST'])
def api_report_item():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    item_type = data.get('item_type')  # 'lost' or 'found'
    user_id = data.get('user_id')
    item = Item(title=title, description=description, item_type=item_type, date_reported=datetime.now(), user_id=user_id)
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': f'{item_type.capitalize()} item reported successfully'})
