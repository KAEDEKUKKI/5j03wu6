from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import main_bp
from .forms import UserGroupForm
from .models import Groups, UserGroup, UserDevice, GroupDevice

@main_bp.route('/permission-management', methods=['GET', 'POST'])
@login_required
def permission_management():
    form = UserGroupForm()

    # Populate choices for user_id and group_id
    form.user_id.choices = [(user.id, user.username) for user in get_all_users()]  # Replace with your user retrieval logic
    form.group_id.choices = [(group.id, group.group_name) for group in Groups.get_all_group()]

    if form.validate_on_submit():
        user_id = form.user_id.data
        group_id = form.group_id.data
        read_permission = form.read_permission.data
        write_permission = form.write_permission.data
        delete_permission = form.delete_permission.data

        user_group = UserGroup.get_by_user_group(user_id, group_id)

        if user_group:
            # Update existing user_group
            user_group.read_p = read_permission
            user_group.write_p = write_permission
            user_group.delete_p = delete_permission
        else:
            # Create a new user_group
            user_group = UserGroup(user_id, group_id, read_permission, write_permission, delete_permission)

        user_group.create()
        flash('Permissions updated successfully!', 'alert-success')
        return redirect(url_for('main.permission_management'))

    return render_template('permission_management.html', form=form)
