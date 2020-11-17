from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from companyFilling.users.forms import RegisterForm, LoginForm
from companyFilling.model import User
from companyFilling import db


fillingForm = Blueprint('fillingForm', __name__)

@login_required
@fillingForm.route('all_form/')
def allCurrentForm():
    return