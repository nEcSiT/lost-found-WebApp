from . import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Item
from .auth import (
    register_user,
    verify_user,
    verify_email_code,
    resend_email_code,
    generate_phone_reset_code,
    verify_phone_code,
    update_user_password,
)
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import uuid

# Photo upload configuration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_photo(photo):
    """Save uploaded photo and return filename"""
    if photo and photo.filename != '':
        if allowed_file(photo.filename):
            # Create unique filename
            file_ext = photo.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
            
            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join(app.root_path, 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save file
            file_path = os.path.join(upload_dir, unique_filename)
            photo.save(file_path)
            
            return unique_filename
    return None

# Landing page: accessible to both authenticated and non-authenticated users
@app.route('/')
def index():
    return render_template('index.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        campus_id = request.form['campus_id']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password', '')
        department = request.form['department']
        phone = request.form['phone']  # Required phone number
        
        try:
            # Server-side validations
            if password != confirm_password:
                flash('Passwords do not match. Please re-enter them.')
                return render_template('register.html')
            if len(password) < 6:
                flash('Password must be at least 6 characters long.')
                return render_template('register.html')
            register_user(name, campus_id, email, password, department, phone)
            flash('Registration successful. Please verify your email to log in.')
            return redirect(url_for('verify_email', email=email))
        except ValueError as e:
            flash(str(e))
        except Exception as e:
            flash('Registration failed. Please try again.')
    
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        campus_id = request.form['campus_id']
        password = request.form['password']
        user = verify_user(campus_id, password)
        if user:
            # Gate login on email verification status
            if not user.email_verified:
                flash('Please verify your email before logging in. A code was sent to your email. You can resend it below.')
                return redirect(url_for('verify_email', email=user.email))
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.')
    return redirect(url_for('index'))

# Dashboard (landing after login)
@app.route('/dashboard')
@login_required
def dashboard():
    recent_items = Item.query.order_by(Item.date_reported.desc()).limit(10).all()
    return render_template('dashboard.html', items=recent_items)

# Report lost item
@app.route('/report_lost', methods=['GET', 'POST'])
@login_required
def report_lost():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        contact_phone = request.form['contact_phone']
        
        # Handle photo upload
        photo_filename = None
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo and photo.filename != '':
                try:
                    photo_filename = save_uploaded_photo(photo)
                    if not photo_filename:
                        flash('Invalid file type. Please upload PNG, JPG, JPEG, or GIF files only.', 'error')
                        return render_template('report_lost.html')
                except Exception as e:
                    flash('Error uploading photo. Please try again.', 'error')
                    return render_template('report_lost.html')
        
        # Create item with photo if uploaded
        item = Item(
            title=title, 
            description=description, 
            item_type='lost', 
            contact_phone=contact_phone,
            date_reported=datetime.now(), 
            user_id=current_user.id,
            photo_filename=photo_filename
        )
        
        try:
            db.session.add(item)
            db.session.commit()
            flash('Lost item reported successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error saving item report. Please try again.', 'error')
    
    return render_template('report_lost.html')

# Report found item
@app.route('/report_found', methods=['GET', 'POST'])
@login_required
def report_found():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        contact_phone = request.form['contact_phone']
        
        # Handle photo upload
        photo_filename = None
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo and photo.filename != '':
                try:
                    photo_filename = save_uploaded_photo(photo)
                    if not photo_filename:
                        flash('Invalid file type. Please upload PNG, JPG, JPEG, or GIF files only.', 'error')
                        return render_template('report_found.html')
                except Exception as e:
                    flash('Error uploading photo. Please try again.', 'error')
                    return render_template('report_found.html')
        
        # Create item with photo if uploaded
        item = Item(
            title=title, 
            description=description, 
            item_type='found', 
            contact_phone=contact_phone,
            date_reported=datetime.now(), 
            user_id=current_user.id,
            photo_filename=photo_filename
        )
        
        try:
            db.session.add(item)
            db.session.commit()
            flash('Found item reported successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error saving item report. Please try again.', 'error')
    
    return render_template('report_found.html')

# Item details page
@app.route('/item/<int:item_id>')
def item_details(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item_details.html', item=item)

# Search functionality for dashboard
@app.route('/search')
def search():
    query = request.args.get('search', '')
    item_type = request.args.get('type', '')
    status = request.args.get('status', '')
    
    items_query = Item.query
    
    if query:
        items_query = items_query.filter(
            Item.title.contains(query) | Item.description.contains(query)
        )
    
    if item_type and item_type != 'all':
        items_query = items_query.filter(Item.item_type == item_type)
    
    if status and status != 'all':
        items_query = items_query.filter(Item.status == status)
    
    items = items_query.order_by(Item.date_reported.desc()).all()
    
    if current_user.is_authenticated:
        return render_template('dashboard.html', items=items)
    else:
        return render_template('index.html', items=items)

@app.route('/about')
def about():
    """About page showcasing the development team"""
    return render_template('about.html')

# Favicon route (to prevent 404 errors)
@app.route('/favicon.ico')
def favicon():
    return '', 204

# Email verification routes
@app.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    if request.method == 'POST':
        email = request.form.get('email')
        code = request.form.get('code')
        if not email or not code:
            flash('Please provide both email and verification code.')
            return render_template('verify_email.html')
        if verify_email_code(email, code):
            flash('Email verified successfully. You can now log in.')
            return redirect(url_for('login'))
        else:
            flash('Invalid verification code or email. Please try again.')
    return render_template('verify_email.html')


@app.route('/resend-email-code', methods=['POST'])
def resend_email():
    email = request.form.get('email')
    if not email:
        flash('Please provide your email to resend the code.')
        return redirect(url_for('verify_email'))
    if resend_email_code(email):
        flash('A new verification code has been sent to your email (check console in dev).')
    else:
        flash('Email not found. Please register first.')
    return redirect(url_for('verify_email'))


# Password reset via Phone OTP
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        phone = request.form.get('phone')
        if not phone:
            flash('Please enter your phone number.')
            return render_template('forgot_password.html')
        if generate_phone_reset_code(phone):
            flash('A verification code has been sent to your phone (check console in dev).')
            return redirect(url_for('verify_reset_code', phone=phone))
        else:
            flash('Phone number not found. Please check and try again.')
    return render_template('forgot_password.html')


@app.route('/verify-reset-code', methods=['GET', 'POST'])
def verify_reset_code():
    phone = request.args.get('phone') or request.form.get('phone')
    if request.method == 'POST':
        code = request.form.get('code')
        if not phone or not code:
            flash('Please provide your phone and the 6-digit code.')
        else:
            user = verify_phone_code(phone, code)
            if user:
                # Pass phone as query so reset form knows it
                return redirect(url_for('reset_password', phone=phone))
            else:
                flash('Invalid code. Please try again.')
    return render_template('verify_reset_code.html', phone=phone)


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    phone = request.args.get('phone') or request.form.get('phone')
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if not phone:
            flash('Missing phone number. Please restart the reset process.')
            return redirect(url_for('forgot_password'))
        if not password or not confirm_password:
            flash('Please enter and confirm your new password.')
            return render_template('reset_password.html', phone=phone)
        if password != confirm_password:
            flash('Passwords do not match.')
            return render_template('reset_password.html', phone=phone)
        if len(password) < 6:
            flash('Password must be at least 6 characters long.')
            return render_template('reset_password.html', phone=phone)

        # Validate the latest code still belongs to this phone (optional) and update password
        user = verify_phone_code(phone, request.form.get('code', '')) or verify_phone_code(phone, request.args.get('code', ''))
        # If no code provided here, assume verification was just completed; find user by phone
        if not user:
            from .models import User
            user = User.query.filter_by(phone=phone).first()
        if not user:
            flash('Could not validate phone for reset. Please try again.')
            return redirect(url_for('forgot_password'))

        update_user_password(user, password)
        flash('Password updated successfully. You can now log in.')
        return redirect(url_for('login'))

    return render_template('reset_password.html', phone=phone)
