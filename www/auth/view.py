from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from . import auth_bp
from .models import Users
from .form import LoginForm, RegistrationForm
from groups.models import Groups,Groups1


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.passwd.data
        remember = form.remember.data

        user = Users.get_by_email(email)
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

        existing_user = Users.get_by_email(email)
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

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user  # 已登入的用戶
    if request.method == 'POST':
        action = request.form.get('action')
        if 'delete_group' in request.form:
            group_name_to_delete = request.form.get('group_name')
            group_id_to_delete = Groups.get_id_by_name(group_name_to_delete)

            flash(f"Group ID to delete: {group_id_to_delete}")
            if group_id_to_delete is not None:
                try:
                    Groups.delete(group_id_to_delete)
                    flash(f"成功刪除組 '{group_id_to_delete}'！", 'success')
                except Exception as e:
                    flash(f"刪除組時出錯: {str(e)}", 'error')
            else:
                flash("未找到对应的组", 'error')


        elif action == 'add':
            user_id = request.form.get('user_id')
            group_id = request.form.get('group_id')

            user_group = Groups1.create(group_id, user_id)
            if user_group:
                flash("成功添加", "success")
            else:
                flash("添加出現錯誤", "danger")

        elif action == 'delete':
            user_id = request.form.get('user_id')
            group_id = request.form.get('group_id')

            user_group = Groups1.delete(group_id, user_id)
            if user_group:
                flash("成功刪除", "success")
            else:
                flash("刪除出現錯誤", "danger")


        elif 'create_group' in request.form:
            group_name = request.form.get('group_name')
            try:
                new_group = Groups.create(group_name=group_name)
                flash(f"成功創建組 '{group_name}'！", 'success')
            except Exception as e:
                flash(f"創建組時出錯: {str(e)}", 'error')


    all_groups = Groups.get_all_group_names()

    return render_template('auth/profile.html', user=user, all_groups=all_groups)