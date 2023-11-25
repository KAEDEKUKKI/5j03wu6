from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class GroupForm(FlaskForm):
    group_name = StringField('Group Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Group_UserForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    inlineFormSelectPref = SelectField('Preference', choices=[], validators=[DataRequired()])
    submit = SubmitField('Add')
