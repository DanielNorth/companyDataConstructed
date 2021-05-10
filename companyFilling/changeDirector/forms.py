from wtforms import StringField, SelectField, TextAreaField, SubmitField, \
                    IntegerField, Form, FieldList, FormField, BooleanField
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired, Length


class DirectorInfo(FlaskForm):
    directorNameInChinese = StringField("New director's name in Chinese", validators=[InputRequired()])
    directorSurname = StringField("New director's English Surname", validators=[validators.optional()])
    directorOtherName = StringField("New director's English Other Name", validators=[InputRequired()])

    previousChineseName = StringField("Previous name in Chinese", validators=[validators.optional()])
    previousEnglishName = StringField("Previous name in English", validators=[validators.optional()])
    chineseAlias = StringField("Alias in Chinese", validators=[validators.optional()])
    englishAlias = StringField("Alias in English", validators=[validators.optional()])

    directorEmail = StringField("Director's email address", validators=[validators.optional()])
    hkidCardNumber = StringField("HKID card number", validators=[validators.optional()])
    passportIssuingCountry = StringField("Passport issuing country", validators=[validators.optional()])
    passportNumber = StringField("Password number", validators=[validators.optional()])

    companyNumber = StringField("Company Number", validators=[validators.optional()])

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