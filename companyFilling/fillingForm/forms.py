from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired, Length


class CompanyForm(FlaskForm):
    companyName = StringField('Company Name: ', validators=[InputRequired(), Length(min=4, max=200)])
    businessName = StringField('Business Name (if any)', validators=[validators.Optional()])
    companyType = SelectField('Type of Company', choices=['Private company ', 'Public company',
                                                          'Company limited by guarantee'])
    date1 = DateField('Date to which this Return is Made Up', format='%d/%m/%Y')
    finanicalStatementStartDate = DateField('Period Covered by Financial Statements Delivered with this Form,'
                                       '(A private company need not complete this section)', format='%d/%m/%Y')
    finanicalStatementEndDate = DateField('To', format='%d/%m/%Y')

    registeredOfficeAddress = TextAreaField('Address of Registered Office')
    emailAddress = StringField('Email address: ')


class AddCompany(FlaskForm):
    companyName = StringField('Company Name: ', validators=[InputRequired(), Length(min=4, max=200)])
    submit = SubmitField('Submit')