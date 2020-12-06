from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired, Length


class Nar1Form(FlaskForm):

    companyName = StringField('Company Name: ', validators=[InputRequired(), Length(min=4, max=300)])
    businessName = StringField('Business Name (if any)', validators=[validators.Optional()])
    companyType = SelectField('Type of Company', choices=['Private company ', 'Public company',
                                                          'Company limited by guarantee'])
    date1 = DateField('Date to which this Return is Made Up', format='%Y-%m-%d', validators=[validators.Optional()])
    financialStatementStartDate = DateField('Period Covered by Financial Statements Delivered with this Form,'
                                       '(A private company need not complete this section)', format='%Y-%m-%d', validators=[validators.Optional()])
    financialStatementEndDate = DateField('To', format='%Y-%m-%d', validators=[validators.Optional()])
    registeredOfficeAddress = TextAreaField('Address of Registered Office', validators=[validators.Optional()])
    emailAddress = StringField('Email address: ', validators=[validators.Optional()])
    mortgagesCharges = TextAreaField("Mortgages and Charges: ", validators=[validators.Optional()])
    q9 = StringField('Number of Member(s) of a Company Not Having a Share Capital', validators=[validators.Optional()])

    f25 = StringField('Class of shares', validators=[validators.Optional()])
    f46 = StringField('Class of shares', validators=[validators.Optional()])
    f47 = StringField('Class of shares', validators=[validators.Optional()])
    f48 = StringField('Class of shares', validators=[validators.Optional()])

    f26 = StringField('Currency', validators=[validators.Optional()])
    f42 = StringField('Currency', validators=[validators.Optional()])
    f43 = StringField('Currency', validators=[validators.Optional()])
    f44 = StringField('Currency', validators=[validators.Optional()])

    # Company Secretary Page
    # header in the html stage that it's for the secretary page
    f50 = StringField('Company Number', validators=[validators.Optional()])

    f51 = StringField('Name in Chinese', validators=[validators.Optional()])
    f52 = StringField('Name in English (Surname)', validators=[validators.Optional()])
    f53 = StringField('Name in English (Other names)', validators=[validators.Optional()])

    f58 = StringField('Hong Kong Address', validators=[validators.Optional()])
    f59 = StringField('Hong Kong Address', validators=[validators.Optional()])
    f60 = StringField('Hong Kong Address', validators=[validators.Optional()])
    f61 = StringField("Email Address", validators=[validators.Optional()])

    f70 = StringField('Company Number', validators=[validators.Optional()])

    # Director 1
    f76 = StringField('Name in Chinese', validators=[validators.Optional()])

    f87 = StringField("Email Address", validators=[validators.Optional()])


    submit = SubmitField("Finish for now", render_kw={"onclick": "Are you sure you want to submit"})


class AddCompany(FlaskForm):
    companyName = StringField('Company Name: ', validators=[InputRequired(), Length(min=4, max=200)])
    submit = SubmitField('Submit')


class aButton(FlaskForm):
    submit = SubmitField('file a new Nar1 form')