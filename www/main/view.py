from flask import render_template
from flask_login import login_required
from . import main_bp
from .models import Groups


@main_bp.route('/')
@login_required
def index():
    return render_template('main/index.html')
  

@main_bp.route('/group')
@login_required
def group():
    all_groups = Groups.get_all_group_names()
    return render_template('auth/group.html', all_groups=all_groups)

