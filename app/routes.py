from . import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Item
from .auth import register_user, verify_user
from datetime import datetime

# Landing page: display recently updated items
@app.route('/')
def index():
    recent_items = Item.query.order_by(Item.date_reported.desc()).limit(10).all()
    return render_template('index.html', items=recent_items)

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        campus_id = request.form['campus_id']
        email = request.form['email']
        password = request.form['password']
        register_user(name, campus_id, email, password)
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = verify_user(email, password)
        if user:
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
    flash('You have been logged out.')
    return redirect(url_for('login'))

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
        item = Item(title=title, description=description, item_type='lost', date_reported=datetime.now(), user_id=current_user.id)
        db.session.add(item)
        db.session.commit()
        flash('Lost item reported successfully!')
        return redirect(url_for('dashboard'))
    return render_template('report_lost.html')

# Report found item
@app.route('/report_found', methods=['GET', 'POST'])
@login_required
def report_found():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        item = Item(title=title, description=description, item_type='found', date_reported=datetime.now(), user_id=current_user.id)
        db.session.add(item)
        db.session.commit()
        flash('Found item reported successfully!')
        return redirect(url_for('dashboard'))
    return render_template('report_found.html')
