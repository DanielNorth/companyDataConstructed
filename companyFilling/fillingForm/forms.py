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
    date1 = DateField('Date to which this Return is Made Up', format='%Y-%m-%d', validators=[validators.optional()])
    financialStatementStartDate = DateField('Period Covered by Financial Statements Delivered with this Form,'
                                       '(A private company need not complete this section)', format='%Y-%m-%d', validators=[validators.optional()])
    financialStatementEndDate = DateField('To', format='%Y-%m-%d', validators=[validators.optional()])

    registeredOfficeAddress = TextAreaField('Address of Registered Office')
    emailAddress = StringField('Email address: ')
    mortgagesCharges = TextAreaField("Mortgages and Charges: ")
    q9 = StringField('Number of Member(s) of a Company Not Having a Share Capital')


    #submit = SubmitField("Finish for now", render_kw={"onclick": "Are you sure you want to submit"})


class AddCompany(FlaskForm):
    companyName = StringField('Company Name: ', validators=[InputRequired(), Length(min=4, max=200)])
    submit = SubmitField('Submit')


class aButton(FlaskForm):
    submit = SubmitField('file a new Nar1 form')