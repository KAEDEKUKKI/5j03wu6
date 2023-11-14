from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
class YourForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    inlineFormSelectPref = SelectField('Preference', choices=[], validators=[DataRequired()])
    submit = SubmitField('Add')