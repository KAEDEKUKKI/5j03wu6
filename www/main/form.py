from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

class ManualConfigForm(FlaskForm):
    device_name = StringField('NAME', validators=[DataRequired()], render_kw={"placeholder": "NAME"})
    device_type = SelectField('Device Type', choices=[], coerce=int)
    ip_address = StringField('IP address', validators=[DataRequired()], render_kw={"placeholder": "IP address"})
    protocol_port = IntegerField('Protocol port', validators=[DataRequired()], render_kw={"placeholder": "Protocol port"})
    submit = SubmitField('SAVE')

class DeviceForm(FlaskForm):
    rm = SubmitField('Delete Device')