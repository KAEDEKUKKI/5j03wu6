from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ManualConfigForm(FlaskForm):
    device_name = StringField('NAME', validators=[DataRequired()], render_kw={"placeholder": "NAME"})
    device_type = StringField('TYPE', validators=[DataRequired()], render_kw={"placeholder": "TYPE"})
    ip_address = StringField('IP address', validators=[DataRequired()], render_kw={"placeholder": "IP address"})
    submit = SubmitField('SAVE')
