from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import Company, Nar1data
from companyFilling import db
from companyFilling.fillingForm.forms import Nar1Form, AddCompany, aButton


fillingForm = Blueprint('fillingForm', __name__)


@fillingForm.route('')
@login_required
def home():
    return render_template('userPage.html', name=current_user.username)


@fillingForm.route('all_company/<company_id>', methods=['GET', 'POST'])
@login_required
def all_form(company_id):
    # only allow to view company that they create
    selectedCompany = Company.query.filter_by(id=company_id).first()
    if str(current_user.id) != str(selectedCompany.owner_id):
        return redirect(url_for('fillingForm.home'))

    else:
        form = aButton()
        companyForm = Nar1data.query.filter_by(company_id=company_id)

        if form.validate_on_submit():
            return redirect(url_for('fillingForm.fill_nar1_form', company_id=selectedCompany.id))
        return render_template('addForm.html', form=form, companyForm=companyForm)


@fillingForm.route('all_company/<company_id>/nar1_form', methods=["POST", 'GET'])
@login_required
def fill_nar1_form(company_id):
    form = Nar1Form()
    if form.validate_on_submit():
        newNar1 = Nar1data(company_id=company_id, companyName=form.companyName.data,
                       businessName=form.businessName.data, typeOfCompany=form.companyType.data,
                       date1=form.date1.data, financialStatementStartDate=form.financialStatementStartDate.data,
                       financialStatementEndDate=form.financialStatementEndDate.data, registeredOfficeAddress=form.registeredOfficeAddress.data,
                       emailAddress=form.emailAddress.data, mortgagesCharges=form.mortgagesCharges.data,
                       q9=form.q9.data)
        db.session.add(newNar1)
        db.session.commit()
        return redirect(url_for('fillingForm.home'))

    return render_template('nar1formTest.html', form=form, name=current_user.username)


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
        newCompany = Company(owner_id=current_user.id, companyName=form.companyName.data)
        db.session.add(newCompany)
        db.session.commit()
        return redirect(url_for('fillingForm.home'))

    return render_template('addCompanyName.html', form=form)

