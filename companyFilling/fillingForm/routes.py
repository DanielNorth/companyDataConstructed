from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import Company
from companyFilling import db
from companyFilling.fillingForm.forms import CompanyForm, AddCompany


fillingForm = Blueprint('fillingForm', __name__)


@fillingForm.route('')
@login_required
def home():
    return render_template('userPage.html', name=current_user.username)


@fillingForm.route('NAR1/')
@login_required
def NAR1():
    form = CompanyForm()
    return render_template('nar1formTest.html', form=form, name=current_user.username)


@fillingForm.route('all_company/<company_id>')
@login_required
def all_form(company_id):
    selectedCompany = Company.query.filter_by(id=company_id).first()
    if str(current_user.id) != str(selectedCompany.owner_id):
        return redirect(url_for('fillingForm.home'))

    else:
        return f'<h1>Fucking tired {selectedCompany.companyName}</h1?>'


@fillingForm.route('all_company/')
@login_required
def all_company():
    companies = Company.query.filter_by(owner_id=current_user.id)
    return render_template('showAllCreatedCompany.html', companies=companies, username=current_user.username)


@fillingForm.route('add_new_company/', methods=['GET', "POST"])
@login_required
def add_new_company():
    form = AddCompany()

    if form.validate_on_submit():
        newCompany = Company(companyName=form.companyName.data, owner_id=current_user.id)
        db.session.add(newCompany)
        db.session.commit()
        return redirect(url_for('fillingForm.home'))

    return render_template('addCompanyName.html', form=form)

