from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired, Email, Length, ValidationError


class CompanyForm(FlaskForm):
    companyName = StringField('Company Name: ', validators=[InputRequired(), Length(min=4, max=200)])
