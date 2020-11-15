from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password: ', validators=[InputRequired(), Length(min=6, max=80)])
    rememberMe = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    confirmedEmail = EmailField('Confirmed Email', [validators.DataRequired(), validators.Email()])
    username = StringField('Username: ', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password: ', validators=[InputRequired(), Length(min=6, max=80)])
    confirmedPassword = PasswordField('Confirmed password: ', validators=[InputRequired(), Length(min=6, max=80)])