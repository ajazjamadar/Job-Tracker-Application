from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .forms import RegisterForm, LoginForm
from .models import User
from . import db, login_manager

# Create auth blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if email already exists
        if User.query.filter_by(email=form.email.data).first():
            current_app.logger.warning(f'Registration attempt with existing email: {form.email.data}')
            flash('Email already registered. Please use a different email.', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new user
        user = User(email=form.email.data, name=form.name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        current_app.logger.info(f'New user registered: {user.email}')
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        # Validate credentials
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            current_app.logger.info(f'User logged in: {user.email}')
            
            # Redirect to next page or dashboard
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.dashboard')
            
            flash(f'Welcome, {user.name or user.email}!', 'success')
            return redirect(next_page)
        else:
            current_app.logger.warning(f'Failed login attempt for email: {form.email.data}')
            flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout route."""
    email = current_user.email if hasattr(current_user, 'email') else 'unknown'
    logout_user()
    current_app.logger.info(f'User logged out: {email}')
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))
