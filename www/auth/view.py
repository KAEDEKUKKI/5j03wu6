from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from . import auth_bp
from .models import Users
from .form import LoginForm, RegistrationForm

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.passwd.data
        remember = form.remember.data

        user = Users.get_user_by_email(email)
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Logged in successfully', 'alert-success')
            next_page = request.args.get('next') or url_for('main.index')
            return redirect(next_page)
        else:
            flash('Invalid email or password', 'alert-danger')

    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data

        existing_user = Users.get_user_by_email(email)
        if existing_user:
            flash('Email address already exists. Please use a different email.', 'alert-danger')
            return redirect(url_for('auth.login'))

        new_user = Users(
            first_name=form.f_name.data,
            last_name=form.l_name.data,
            email=email
        )
        new_user.set_password(form.passwd.data, form.confirm_password.data)
        user_id = new_user.create()

        if user_id:
            flash('Registration success', 'alert-success')
            return redirect(url_for('auth.login'))
        else:
            flash('Failed to register user', 'alert-danger')

    return render_template('auth/register.html', form=form)

@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user = current_user  # 已登入的用戶
    return render_template('auth/profile.html', user=user)

