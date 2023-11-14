from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from . import main_bp
from .models import Groups,Groups1
from .form import YourForm  

@main_bp.route('/')
@login_required
def index():
    return render_template('main/index.html')

@main_bp.route('/group', methods=['GET', 'POST'])
@login_required
def group():
    form = YourForm() 
    if request.method == 'POST' and form.validate_on_submit():
        user_id = form.user_id.data
        group_id = form.inlineFormSelectPref.data 

        # 創新用戶組
        user_group = Groups1.create(group_id, user_id)
        if user_group:
            flash("成功添加", "success")
            return redirect(url_for("main_bp.group"))
        else:
                flash("添加出现錯誤", "danger")
    else:
        flash("無法找到匹配的组", "danger")
    all_groups = Groups.get_all_group_names()
    form.inlineFormSelectPref.choices = [(group['id'], group['group_name']) for group in all_groups]


    return render_template('auth/group.html',form=form)
