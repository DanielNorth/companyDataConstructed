from wtforms import StringField, SelectField, TextAreaField, SubmitField, \
                    IntegerField, Form, FieldList, FormField, BooleanField
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired, Length


class CompanyInfo(FlaskForm):
    companyChineseName = StringField("Company Chinese Name:", validators=[validators.Optional()])
    companyName = StringField('Company English Name: ', validators=[InputRequired(), Length(min=4, max=300)])
    businessName = StringField("Business Name(if any):", validators=[validators.Optional()])
    submit = SubmitField("Input the rest of the information", render_kw={"onclick": "Are you sure you want to submit"})

    addressOfRegisteredOffice1 = StringField("Address of registered office (line 1)", validators=[validators.Optional()])
    addressOfRegisteredOffice2 = StringField("Address of registered office (line 2)", validators=[validators.Optional()])
    addressOfRegisteredOffice3 = StringField("Address of registered office (line 3)", validators=[validators.Optional()])
    companyEmail = StringField("Company Email Address", validators=[validators.Optional()])

    nonShareHolder = IntegerField("Number of Member(s) of a Company Not Having a Share Capital", validators=[validators.Optional()])

    shareClass = StringField("Name of Share Class:", default="Ordinary")
    shares_issued = IntegerField("Total Number of shares you want to issue", validators=[validators.Optional()])
    currency = SelectField("Currency", choices=["USD", "HKD", "EUR", "JPY", "GBP", "AUD", "CAD", "CNY", "CHF",
                                                "NZD", "SEK", "KRW", "SGD", "NOK", "MXN", "INR", "RUB", "ZAR"])
    #totalAmount = IntegerField("Total Amount", validators=[InputRequired()], render_kw={"placeholder": 1})
    totalAmount = IntegerField("Total Amount", validators=[InputRequired()])
    totalPaidUp = IntegerField("Total Paid up or Registered as Paid up", validators=[InputRequired()])


class DirectorInfo(FlaskForm):
    directorNameInChinese = StringField("New director's name in Chinese", validators=[InputRequired()])
    directorSurname = StringField("New director's English Surname", validators=[validators.optional()])
    directorOtherName = StringField("New director's English Other Name", validators=[validators.Optional()])

    englishName = StringField("New director's company english name", validators=[validators.Optional()])

    previousChineseName = StringField("Previous name in Chinese", validators=[validators.Optional()])
    previousEnglishName = StringField("Previous name in English", validators=[validators.Optional()])
    chineseAlias = StringField("Alias in Chinese", validators=[validators.Optional()])
    englishAlias = StringField("Alias in English", validators=[validators.Optional()])

    address1 = StringField("Address (Line 1): ", validators=[validators.Optional()])
    address2 = StringField("Address (Line 2): ", validators=[validators.Optional()])
    address3 = StringField("Address (Line 3): ", validators=[validators.Optional()])

    directorEmail = StringField("Director's email address", validators=[validators.Optional()])
    hkidCardNumber = StringField("HKID card number", validators=[validators.optional(), Length(max=8)])
    passportIssuingCountry = StringField("Passport issuing country", validators=[validators.Optional()])
    passportNumber = StringField("Passport number", validators=[validators.Optional()])

    companyNumber = StringField("Company Number", validators=[validators.Optional()])

    naturalPerson = SelectField("Director Status", choices=["Natural Person"], validators=[validators.Optional()])
    corporate = SelectField("Director Status", choices=["Corporate"], validators=[validators.Optional()])

    alreadyADirector = SelectField("Is the resigning appointed director still hold a alternate director/director position in the company after cessation date?",
                                   choices=["no", 'yes'], validators=[validators.Optional()])
    cessationReason = SelectField("Reason of cessation", choices=["Resignation/Others", "Deceased"], validators=[validators.Optional()])

    alreadyADirectorB = SelectField("Did the newly appointed director already hold an alternate director/director position in the company before?",
                                    choices=["no", 'yes'], validators=[validators.Optional()])

    submit = SubmitField("Finish for now", render_kw={"onclick": "return confirm('Are you sure?')"})


class SubmitButton(FlaskForm):
    submit = SubmitField("My information is correct", render_kw={"onclick": "return confirm('Are you sure?')",
                                                                 "class": "hs-button primary large action-button"})
