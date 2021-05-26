from wtforms import StringField, SelectField, TextAreaField, SubmitField, \
                    IntegerField, Form, FieldList, FormField, BooleanField
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired, Length


class ShareInfo(FlaskForm):
    name = StringField("Share holder name")
    shareClass = StringField("Share Class", validators=[validators.Optional()])
    totalShares = IntegerField("Total Share", validators=[validators.Optional()])
    address = StringField("Address", validators=[validators.Optional()])
    submit = SubmitField("Submit")


class ShareTransferForm(FlaskForm):
    shareClass = StringField("Share Class", validators=[validators.Optional()])
    totalShares = IntegerField("Total Share Transfer", validators=[validators.Optional()])

    transferTo = StringField("New shareholder name", validators=[validators.Optional()])
    transferDate = DateField('Date of transfer', format='%Y-%m-%d', validators=[validators.Optional()])

    submit = SubmitField("Submit")


class ShareCapitalForm(FlaskForm):
    totalNumber = StringField("Total number of share", validators=[InputRequired()])
    currency = SelectField("Currency", choices=["USD", "HKD", "EUR", "JPY", "GBP", "AUD", "CAD", "CNY", "CHF",
                                                "NZD", "SEK", "KRW", "SGD", "NOK", "MXN", "INR", "RUB", "ZAR"])
    totalAmount = StringField("Total Amount")
    totalPaidUp = StringField("Total Paid up or Registered as Paid up")

    submit = SubmitField("Submit")
