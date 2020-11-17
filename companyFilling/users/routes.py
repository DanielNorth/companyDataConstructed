from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from companyFilling.users.forms import RegisterForm, LoginForm
from companyFilling.model import User
from companyFilling import db

users = Blueprint('users', __name__)


@users.route('register/', methods=['GET', 'POST'], endpoint='register/')
def registerUser():
    form = RegisterForm()

    if form.validate_on_submit():
        if (form.email.data == form.confirmedEmail.data) and (form.password.data == form.confirmedPassword.data):
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            newUser = User(username=form.username.data, email=form.email.data,
                           password=hashed_password)
            db.session.add(newUser)
            db.session.commit()
            return "<h1>New user created</h1>"
        else:
            flash('seems like the confirmed email or password doesn\'s match')

    return render_template('register.html', form=form)


@users.route('login/', methods=['GET', "POST"], endpoint='login/')
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        if email:
            if check_password_hash(email.password, form.password.data):
                return '<h1>' + "Hello " + form.email.data + email.password + '</h1>'
        else:
            return '<h1>Nothing</h1>'

    return render_template('login.html', form=form)

