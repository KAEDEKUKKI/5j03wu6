from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user
from . import auth_bp
from .models import Users
from .form import LoginForm, RegistrationForm

@auth_bp.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.passwd.data
        remember = form.remember.data
        # check if password is matched
        user = Users.get_user_by_email(email, password)
        if user :
            login_user(user, remember=remember)
            flash('Logged in successfully', 'success')
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            flash('Invalid email or password', 'error')
    return render_template('auth/login.html', form = form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@auth_bp.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        f_name = form.f_name.data
        l_name = form.l_name.data
        email = form.email.data
        password = form.passwd.data
        check_password = form.confirm_password.data
        existing_user = Users.get_user_by_email(email)
        if existing_user:
            flash('Email address already exists. Please use a different email.', 'danger')
            return redirect(url_for('auth.login'))
        new_user = Users(first_name=f_name, last_name=l_name, email=email)
        new_user.set_password(password, check_password)
        user_id = new_user.create()
        if user_id:
            flash('Registration success', category="success")
            return redirect(url_for('auth.login'))
        else:
            flash('Failed to register user', category="error")
    return render_template('auth/register.html', form = form)
