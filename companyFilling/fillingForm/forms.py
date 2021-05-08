from wtforms import StringField, SelectField, TextAreaField, SubmitField, \
                    IntegerField, Form, FieldList, FormField, BooleanField
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired, Length


class Nar1Form(FlaskForm):

    companyName = StringField('Company Name: ', validators=[InputRequired(), Length(min=4, max=300)])
    S2compName = StringField('Business Name (if any)', validators=[validators.Optional()])
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

    f27 = StringField("Total Number of issued Shares", validators=[validators.Optional()])
    f38 = StringField("Total Number of issued Shares", validators=[validators.Optional()])
    f39 = StringField("Total Number of issued Shares", validators=[validators.Optional()])
    f40 = StringField("Total Number of issued Shares", validators=[validators.Optional()])

    f28 = StringField("Total Amount of issued Shares", validators=[validators.Optional()])
    f34 = StringField("Total Number of issued Shares", validators=[validators.Optional()])
    f35 = StringField("Total Number of issued Shares", validators=[validators.Optional()])
    f36 = StringField("Total Number of issued Shares", validators=[validators.Optional()])

    f29 = StringField("Total amount paid up or regarded as paid up", validators=[validators.Optional()])
    f30 = StringField("Total amount paid up or regarded as paid up", validators=[validators.Optional()])
    f31 = StringField("Total amount paid up or regarded as paid up", validators=[validators.Optional()])
    f32 = StringField("Total amount paid up or regarded as paid up", validators=[validators.Optional()])

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
    f62 = StringField("Passport issued Country", validators=[validators.Optional()])
    f63 = StringField("Passport Number", validators=[validators.Optional()])


    f70 = StringField('Company Number', validators=[validators.Optional()])

    # Director 1
    f76 = StringField('Name in Chinese', validators=[validators.Optional()])

    f87 = StringField("Email Address", validators=[validators.Optional()])


    submit = SubmitField("Finish for now", render_kw={"onclick": "Are you sure you want to submit"})


class AddCompany(FlaskForm):
    companyName = StringField('Company Name: ', validators=[InputRequired(), Length(min=4, max=200)])
    typeOfCompany = SelectField("Type of company", choices=["Private Company", "Public Company",
                                                            "Company limited by guarantee"])
    submit = SubmitField('Submit')


class aButton(FlaskForm):
    submit = SubmitField('file a new Nar1 form')


class Director(Form):
    name = StringField("Directors Name")
    idNumber = StringField("Director HKID number")
    PassportCountry = StringField("Director Passport issued Country")
    PassportNum = StringField("Director passport number")


class ShareCapital(Form):
    classOfShares = StringField("Class of shares")
    currency = StringField("Currency")
    totalNumber = IntegerField("total number")
    totalAmount = IntegerField("total amount")
    totalPaidUp = IntegerField("Total Amount Paid up or Registered as Paid up")


class CompanyInfo(FlaskForm):
    companyName = StringField('Company Name: ', validators=[InputRequired(), Length(min=4, max=300)])
    businessName = StringField("Business Name(if any):", validators=[validators.optional()])
    companyNumber = StringField("Company Number", validators=[validators.Optional()])
    submit = SubmitField("Finish for now", render_kw={"onclick": "Are you sure you want to submit"})

    typeOfCompany = SelectField("Type of company", choices=["Private Company", "Public Company",
                                                            "Company limited by guarantee"])

    addressOfRegisteredOffice1 = StringField("Address of registered office", validators=[validators.Optional()])
    addressOfRegisteredOffice2 = StringField("Address of registered office", validators=[validators.Optional()])
    addressOfRegisteredOffice3 = StringField("Address of registered office", validators=[validators.Optional()])
    addressOfRegisteredOfficeRegion = StringField("Region", validators=[validators.Optional()])
    companyEmail = StringField("Email Address", validators=[validators.Optional()])


    nonShareHolder = IntegerField("Number of Member(s) of a Company Not Having a Share Capital", validators=[validators.optional()])
    shares_issued = IntegerField("Total Number of shares issued")

    number_of_directors = IntegerField('Number of director(s)', [validators.NumberRange(min=0, max=50)])
    director = FieldList(FormField(Director), min_entries=0, max_entries=20)
    #shareCapital = FieldList(FormField(ShareCapital), min_entries=0)

    registeredOfficeAddress = StringField("Address of Registered Office", validators=[validators.optional()])

