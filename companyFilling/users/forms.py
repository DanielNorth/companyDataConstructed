from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired, Email, Length, ValidationError
from companyFilling.model import User


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[InputRequired(), Length(min=4, max=80)])
    password = PasswordField('Password: ', validators=[InputRequired(), Length(min=6, max=80)])
    rememberMe = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    confirmedEmail = EmailField('Confirmed Email', [validators.DataRequired(), validators.Email()])
    username = StringField('Username: ', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password: ', validators=[InputRequired(), Length(min=6, max=80)])
    confirmedPassword = PasswordField('Confirmed password: ', validators=[InputRequired(), Length(min=6, max=80)])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exist")


class ResetPasswordForm(FlaskForm):
    email = EmailField('Email', [validators.DataRequired(), validators.Email()], render_kw={"placeholder": "Enter Email Address",
                                                                                            'class': "form-control form-control-user",
                                                                                            'id': "exampleInputEmail",
                                                                                            'aria - describedby': "emailHelp",
                                                                                            'type': "email"})


class NewPassword(FlaskForm):
    newPassword = PasswordField('New password: ', validators=[InputRequired(), Length(min=6, max=80)])
    confirmedNewPassword = PasswordField('Confirmed password: ', validators=[InputRequired(), Length(min=6, max=80)])


class PasswordChange(FlaskForm):
    oldPassword = PasswordField("Old password: ", validators=[InputRequired(), Length(min=6, max=80)])
    newPassword = PasswordField("New password: ", validators=[InputRequired(), Length(min=6, max=80)])
    confirmedNewPassword = PasswordField("Confirmed New password", validators=[InputRequired(), Length(min=6, max=80)])

    submit = SubmitField("Confirm", render_kw={"class": "btn btn-primary",
                                               "color": "red"})