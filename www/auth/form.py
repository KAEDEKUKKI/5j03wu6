from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo
        
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()],render_kw={"placeholder": "EMAIL"})
    passwd = PasswordField('Password', validators = [DataRequired(), Length(min=6)], render_kw={"placeholder": "PASSWORD"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    f_name = StringField('Frist Name', validators=[DataRequired(message='Fist Name is required.'), Length(max=20)])
    l_name = StringField('Last Name', validators=[Length(max=50)])
    email = StringField('Email', validators=[DataRequired(message='Email is required.'), Email()])
    passwd = PasswordField('Password', validators=[DataRequired(message='Password is required.'), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('passwd', message='Passwords must match.')
    ])
    submit = SubmitField('Register')

