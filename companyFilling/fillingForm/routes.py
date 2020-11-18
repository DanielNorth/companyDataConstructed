from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import User
from companyFilling import db
from companyFilling.fillingForm.forms import CompanyForm


fillingForm = Blueprint('fillingForm', __name__)


@fillingForm.route('all_form/')
@login_required
def all_form():
    return render_template('userPage.html', name=current_user.username)


@fillingForm.route('NAR1/')
@login_required
def NAR1():
    form = CompanyForm()
    return render_template('nar1form.html', form=form)