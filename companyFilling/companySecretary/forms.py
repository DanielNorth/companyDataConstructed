from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired, Email, Length, ValidationError
from companyFilling.model import User


class SecretaryInfo(FlaskForm):
    nameInChinese = StringField("Name in Chinese:", validators=[validators.required()])
    englishGivenName = StringField("English Given name:", validators=[validators.optional()])
    englishName = StringField("English name", validators=[validators.optional()])
    previousChineseName = StringField("Previous Chinese name", validators=[validators.optional()])
    previousEnglishName = StringField("Previous English name", validators=[validators.optional()])
    chineseAliasName = StringField("Chinese Alias Name", validators=[validators.optional()])
    englishAliasName = StringField("English Alias Name", validators=[validators.optional()])

    hkIDcardNumber = StringField("Hong Kong Identity card number", validators=[validators.optional()])
    passportIssuedCountry = StringField("Passport Issuing Country", validators=[validators.optional()])
    passportNumber = StringField("Passport Number", validators=[validators.optional()])

    companyNumber = StringField("Compnay Number", validators=[validators.optional()])
    email = StringField("Email Address", validators=[validators.optional()])
    companyName = StringField("Company Name", validators=[validators.optional()])

    address1 = StringField("Company Address Line 1:", validators=[validators.optional()])
    address2 = StringField("Company Address Line 2:", validators=[validators.optional()])
    address3 = StringField("Company Address Line 3:", validators=[validators.optional()])

    companyOrPerson = SelectField("Nature Person or body Corporate", choices=["Natural Person", "Body Corporate"])

    submit = SubmitField("Submit")

