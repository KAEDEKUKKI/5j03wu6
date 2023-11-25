from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from . import group_bp
from .models import Groups,Groups1
from .form import Group_UserForm ,GroupForm 



# @group_bp.route('/group', methods=['GET', 'POST'])
# @login_required
# def group():
#     form = Group_UserForm() 
#     if request.method == 'POST' and form.validate_on_submit():
#         user_id = form.user_id.data
#         group_id = form.inlineFormSelectPref.data 

#         # 創新用戶組
#         user_group = Groups1.create(group_id, user_id)
#         if user_group:
#             flash("成功添加", "success")
#             return redirect(url_for("main_bp.group"))
#         else:
#             flash("添加出现錯誤", "danger")
#     else:
#         flash("無法找到匹配的组", "danger")
#     all_groups = Groups.get_all_group_names()
#     form.inlineFormSelectPref.choices = [(group['id'], group['group_name']) for group in all_groups]
#     return render_template('auth/group.html',form=form)


# @group_bp.route('/group', methods=['GET', 'POST'])
# @login_required
# def group():
#     form = GroupForm()

#     if form.validate_on_submit():
#         group_name = form.group_name.data
#         try:
#             new_group = Groups.create(group_name=group_name)
#             flash(f"成功創建組 '{group_name}'！", 'success')
#             return redirect(url_for('group_bp.group_profile'))
#         except Exception as e:
#             flash(f"創建組時出錯: {str(e)}", 'error')

#     return render_template('auth/profile.html', form=form)

