from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms import validators
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm


class SubmitButton(FlaskForm):
    submit = SubmitField("Submit Signature")