from flask import render_template, Blueprint, request, redirect, flash
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import InputRequired, Email, Length, ValidationError

homePage = Blueprint('homePage', __name__)


@homePage.route('/', methods=["POST", "GET"])
def homepage():
    form = ContactUs()

    if request.method == 'POST':
        from companyFilling.users.utils import send_email_to_myself
        messageBody = f"Name: {form.name.data}, email: {form.email.data}\n"
        messageBody += form.message.data
        send_email_to_myself(form.subject.data, messageBody)

        flash("Your message has been sent, thanks for reaching to us")

    return render_template('landingPage/betterHomePage.html', form=form)


@homePage.route("contact/<name>")
def contact_us(name):
    form = ContactUs()

    return render_template("landingPage/contact_us", form=form)


class ContactUs(FlaskForm):
    name = StringField("", render_kw={"placeholder": "Name"})
    email = EmailField("", render_kw={"placeholder": "Email"})
    subject = StringField("", render_kw={"placeholder": "Subject"})
    message = StringField("", render_kw={"placeholder": "Message"})