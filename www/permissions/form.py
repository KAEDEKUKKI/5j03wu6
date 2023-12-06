from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField, SubmitField

class UserGroupForm(FlaskForm):
    user_id = SelectField('User ID', coerce=int)
    group_id = SelectField('Group ID', coerce=int)
    read_permission = BooleanField('Read Permission')
    write_permission = BooleanField('Write Permission')
    delete_permission = BooleanField('Delete Permission')
    submit = SubmitField('Save')
