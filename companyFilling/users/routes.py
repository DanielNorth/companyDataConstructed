from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from companyFilling.users.forms import RegisterForm, LoginForm, ResetPasswordForm, NewPassword
from companyFilling.model import User, UserMessage
from companyFilling import db, mail
from companyFilling.users.utils import send_reset_email, send_confirmation_mail
from flask_mail import Message

users = Blueprint('users', __name__)


@users.route('register/', methods=['GET', 'POST'], endpoint='register/')
def registerUser():
    form = RegisterForm()

    if form.validate_on_submit():
        if (form.email.data == form.confirmedEmail.data) and (form.password.data == form.confirmedPassword.data):
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            newUser = User(username=form.username.data, email=form.email.data,
                           password=hashed_password, ownedCompany=0)
            db.session.add(newUser)
            db.session.commit()
            send_confirmation_mail(newUser)
            return "<h1>New user created</h1>"
        else:
            flash('seems like the confirmed email or password doesn\'t match')

    return render_template('users/register.html', form=form)


@users.route('login/', methods=['GET', "POST"], endpoint='login/')
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        if email:
            if check_password_hash(email.password, form.password.data):
                login_user(email, remember=form.rememberMe.data)
                return redirect(url_for('fillingForm.home'))
            else:
                flash('Incorrect email or password')
        else:
            flash('Incorrect email or password', 'warning')

    return render_template('users/login.html', form=form)


@users.route('logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login/'))


@users.route('/reset_password', methods=["GET", "POST"])
def reset_request():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('An email has been send')
            return redirect(url_for('users.login/'))
        else:
            flash("The email doesn't exist in our database")
        #
        # else:
        #     flash("Email doesn't exist")

    return render_template('users/forgot-password.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_token(token):

    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid Token", 'warning')
        return redirect(url_for('users.reset_request'))

    form = NewPassword()
    if form.validate_on_submit():
        if form.newPassword.data == form.confirmedNewPassword.data:
            hashed_password = generate_password_hash(form.newPassword.data, method='sha256')
            user.password = hashed_password
            db.session.commit()
            flash("your password is reset, you are now able to log in")
            return redirect(url_for('users.login/'))

    return render_template('users/reset_password.html', title='Reset Password', form=form)


@users.route("confirm_email/<token>")
def confirm_email(token):
    user = User.verify_reset_token(token=token)
    if user is None:
        return "<h1>Sorry, there is an error and we can not confirm the email for now. Please try later</h1>"
    else:
        user.emailConfirmed = True
        db.session.commit()
        return render_template('users/emailConfirmed.html')


@users.route("profile/password_change", methods=['POST', "GET"])
@login_required
def password_change():
    from .forms import PasswordChange
    form = PasswordChange()

    if form.validate_on_submit():
        oldPassword = User.query.filter_by(id=current_user.id).first()
        if (form.newPassword.data == form.confirmedNewPassword.data) and check_password_hash(oldPassword.password, form.oldPassword.data):
            oldPassword.password = generate_password_hash(form.confirmedNewPassword.data, method='sha256')
            db.session.commit()

            return redirect("https://www.youtube.com/watch?v=a_XgQhMPeEQ&ab_channel=FleetwoodMacFleetwoodMacOfficialArtistChannel")

    return render_template("users/password_change.html", form=form)


@users.route('profile1')
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()

    return render_template('users/profile.html', user=user)


@users.route("message_centre")
@login_required
def message_centre():
    messages = UserMessage.query.filter_by(user_id=current_user.id).order_by(UserMessage.id.desc()).all()

    return render_template('users/messageCentre.html', messages=messages)


@users.route("message/<message_id>")
@login_required
def message_detail(message_id):
    message = UserMessage.query.filter_by(id=message_id).first()
    if not message.read:
        message.read = True
        db.session.commit()

    return render_template('users/messageDetail.html', message=message)


