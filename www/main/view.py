from flask import render_template,request, redirect, url_for,flash
from flask_login import login_required
from . import main_bp
from .models import Groups,Groups1


@main_bp.route('/')
@login_required
def index():
    return render_template('main/index.html')
  

@main_bp.route('/group', methods=['GET', 'POST'])
@login_required
def group():
    if request.method == 'POST':
        userid = request.form.get('user_id')
        groupid = request.form.get('group_id')


        result =Groups1.create(group_id=groupid, user_id=userid)
        print(f"Result of Groups1.create: {result}")
        if result:
             flash('用户添加到组成功', 'success')
        else:
            flash('无法添加用户到组，请检查日志以获取详细信息', 'error')
    


        return redirect(url_for('main.group'))

    all_groups = Groups.get_all_group_names()

    return render_template('auth/group.html', all_groups=all_groups)

