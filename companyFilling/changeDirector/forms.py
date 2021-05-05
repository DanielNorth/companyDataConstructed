from wtforms import StringField, SelectField, TextAreaField, SubmitField, \
                    IntegerField, Form, FieldList, FormField
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired, Length


class DirectorInfo(FlaskForm):
    directorNameInChinese = StringField("New director's name in Chinese", validators=[InputRequired()])
    directorNameInEnglish = StringField("New director's name in English", validators=[InputRequired()])
    directorEmail = StringField("Director's email address", validators=[InputRequired()])
    hkidCardNumber = StringField("HKID card number", validators=[InputRequired()])
    passportIssuingCountry = StringField("Passport issuing country")
    passportNumber = StringField("Password number", validators=[InputRequired()])
