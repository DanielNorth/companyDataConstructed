from flask import render_template, url_for, flash, redirect, send_file, Blueprint, abort, request
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import DirectorResignation, Company, Director, ShareHolderStake, ShareCapital
from companyFilling import db
from companyFilling.changeDirector.forms import Test
import os
import uuid
from datetime import date
from .forms import CompanyInfo

incorporate_new_company = Blueprint('incorporate_new_company', __name__)


@incorporate_new_company.route("", methods=["POST", "GET"])
@login_required
def new_company():
    form = CompanyInfo()

    if request.method == "POST":
        newCompany = Company(companyName=form.companyName.data, companyChineseName=form.companyChineseName.data,
                             companyEmail=form.companyEmail.data, businessName=form.businessName.data,
                             addressOfRegisteredOffice1=form.addressOfRegisteredOffice1.data,
                             addressOfRegisteredOffice2=form.addressOfRegisteredOffice2.data,
                             addressOfRegisteredOffice3=form.addressOfRegisteredOffice3.data,
                             owner_id=current_user.id)
        db.session.add(newCompany)
        db.session.commit()

        newShareCaptial = ShareCapital(company_id=newCompany.id, shareClass=form.shareClass.data,
                                       currency=form.currency.data, totalNumber=form.shares_issued.data,
                                       totalAmount=form.totalAmount.data, totalPaidUp=form.totalPaidUp.data)
        db.session.add(newShareCaptial)
        db.session.commit()

        return redirect(url_for('incorporate_new_company.add_person', company_id=newCompany.id, total_shares=form.shares_issued.data,
                                pageNumber=1))

    return render_template('newCompany/multi-step-form.html', form=form)


@incorporate_new_company.route("directors_founders/<company_id>/<total_shares>", methods=["POST", "GET"])
@login_required
def add_person(company_id, total_shares):

    if request.method == "POST":
        return redirect(url_for("incorporate_new_company.review", company_id=company_id))

    return render_template("newCompany/multi-step-form2.html", company_id=company_id, total_shares=total_shares)


@incorporate_new_company.route('add_director/<company_id>', methods=['GET', "POST"])
@login_required
def add_director(company_id):
    company = Company.query.filter_by(id=company_id).first()
    if company.owner_id != current_user.id:
        abort(403)

    from .forms import DirectorInfo

    form = DirectorInfo()
    if form.validate_on_submit():
        # if request.form.get("reason") == "AlternateDirector":
        #     alternateToWho = request.form.get('alternateTo')
        today = date.today()

        newDirector = Director(company_id=company_id, directorNameInChinese=form.directorNameInChinese.data,
                               directorSurname=form.directorSurname.data, directorOtherName=form.directorOtherName.data,
                               hkidCardNumber=form.hkidCardNumber.data,
                               directorEmail=form.directorEmail.data, passportIssuingCountry=form.passportIssuingCountry.data,
                               passportNumber=form.passportNumber.data, companyOwnerID=current_user.id,
                               companyOrPerson="Natural Person", capacity=request.form.get("reason"),
                               alternateTo=request.form.get('alternateTo'), address1=form.address1.data,
                               address2=form.address2.data, address3=form.address3.data,
                               dateAdded=today.strftime("%B %d, %Y"), active="active")

        db.session.add(newDirector)
        db.session.commit()

        return "<script>window.close();</script>"

    return render_template("changeDirector/addDirector.html", form=form)


@incorporate_new_company.route('add_director_corp/<company_id>', methods=['GET', "POST"])
@login_required
def add_director_corp(company_id):
    company = Company.query.filter_by(id=company_id).first()
    if company.owner_id != current_user.id:
        abort(403)

    from .forms import DirectorInfo

    form = DirectorInfo()
    if form.validate_on_submit():
        today = date.today()
        newDirector = Director(company_id=company_id, directorNameInChinese=form.directorNameInChinese.data,
                               directorOtherName=form.englishName.data, directorEmail=form.directorEmail.data,
                               companyOwnerID=current_user.id, companyOrPerson="Corporate",
                               capacity=request.form.get("reason"),
                               alternateTo=request.form.get('alternateTo'), companyNumber=form.companyNumber.data,
                               address1=form.address1.data, address2=form.address2.data,
                               address3=form.address3.data, dateAdded=today.strftime("%B %d, %Y"),
                               active="active", directorSurname=""
                               )

        db.session.add(newDirector)
        db.session.commit()

        return """<script><script type='text/javascript'>
    window.open('','_parent',''); 
    window.close();
</script>"""
    return render_template("changeDirector/addDirectorCorp.html", form=form)


@incorporate_new_company.route("add_existing_shareholder/<company_id>/<total_shares>", methods=["POST", "GET"])
@login_required
def add_existing_shareholder(company_id, total_shares):
    from companyFilling.shareHolder.forms import ShareInfo
    from companyFilling.model import ShareCapital

    form = ShareInfo()
    try:
        share_clas = ShareCapital.query.filter_by(company_id=company_id).all()
        share_classes = []
        for i in share_clas:
            if i.shareClass not in share_classes:
                share_classes.append(i.shareClass)
    except:
        share_classes = []

    if form.validate_on_submit():
        if request.form.get("shareOfClass") == "":
            shareClass = str(request.form.get('other_class'))
        else:
            shareClass = str(request.form.get("shareOfClass"))

        existingShareHolder = ShareHolderStake(name=form.name.data, shareClass=' '.join(shareClass.split()),
                                               totalShares=form.totalShares.data, address=form.address.data,
                                               company_id=company_id, email=form.email.data)
        db.session.add(existingShareHolder)
        db.session.commit()
        return redirect(url_for("fillingForm.edit_company_info", company_id=company_id))

    return render_template('shareHolder/addExistingShareHolder.html', company_id=company_id, form=form, share_classes=share_classes,
                           total_shares=total_shares)


@incorporate_new_company.route("review/<company_id>", methods=["POST", "GET"])
@login_required
def review(company_id):
    company = Company.query.filter_by(id=company_id).first()
    shareHolders = ShareHolderStake.query.filter_by(company_id=company_id).all()
    directors = Director.query.filter_by(company_id=company_id).all()

    return render_template('newCompany/review.html', company=company, share_holders=shareHolders,
                           directors=directors)