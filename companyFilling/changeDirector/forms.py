from wtforms import StringField, SelectField, TextAreaField, SubmitField, \
                    IntegerField, Form, FieldList, FormField, BooleanField
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired, Length


class DirectorInfo(FlaskForm):
    directorNameInChinese = StringField("New director's name in Chinese", validators=[InputRequired()])
    directorSurname = StringField("New director's English Surname", validators=[validators.optional()])
    directorOtherName = StringField("New director's English Other Name", validators=[validators.optional()])

    englishName = StringField("New director's company english name", validators=[validators.optional()])

    previousChineseName = StringField("Previous name in Chinese", validators=[validators.optional()])
    previousEnglishName = StringField("Previous name in English", validators=[validators.optional()])
    chineseAlias = StringField("Alias in Chinese", validators=[validators.optional()])
    englishAlias = StringField("Alias in English", validators=[validators.optional()])

    address1 = StringField("Address (Line 1): ", validators=[validators.optional()])
    address2 = StringField("Address (Line 2): ", validators=[validators.optional()])
    address3 = StringField("Address (Line 3): ", validators=[validators.optional()])

    directorEmail = StringField("Director's email address", validators=[validators.optional()])
    hkidCardNumber = StringField("HKID card number", validators=[validators.optional(), Length(max=8)])
    passportIssuingCountry = StringField("Passport issuing country", validators=[validators.optional()])
    passportNumber = StringField("Passport number", validators=[validators.optional()])

    companyNumber = StringField("Company Number", validators=[validators.optional()])

    naturalPerson = SelectField("Director Status", choices=["Natural Person"], validators=[validators.optional()])
    corporate = SelectField("Director Status", choices=["Corporate"], validators=[validators.optional()])

    alreadyADirector = SelectField("Is the resigning appointed director still hold a alternate director/director position in the company after cessation date?",
                                   choices=["no", 'yes'], validators=[validators.optional()])
    cessationReason = SelectField("Reason of cessation", choices=["Resignation/Others", "Deceased"], validators=[validators.optional()])

    alreadyADirectorB = SelectField("Did the newly appointed director already hold an alternate director/director position in the company before?",
                                    choices=["no", 'yes'], validators=[validators.optional()])

    submit = SubmitField("Finish for now", render_kw={"onclick": "Are you sure you want to submit"})


# class MyForm(FlaskForm):
#
#     def __init__(self, songs, **kw):
#         super(MyForm, self).__init__(**kw)
#         self.name.songs = songs
#
#     name = SelectField("Song Name", choices=[i for i in self.name.songs.text])

class Test(FlaskForm):
    submit = SubmitField("Submit")