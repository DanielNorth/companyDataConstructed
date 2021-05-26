from flask import render_template, url_for, flash, redirect, send_file, Blueprint, abort, request
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import Company, Nar1data, Director, Secretary
from companyFilling import db
from companyFilling.changeDirector.forms import DirectorInfo
import os
from companyFilling.companySecretary.forms import SecretaryInfo

companySecretary = Blueprint("companySecretary", __name__)


@companySecretary.route("change_secretary", methods=["POST", "GET"])
@login_required
def change_secretary():
    form = SecretaryInfo()

    return render_template("changeSecretary/newSecretary.html", form=form)


@companySecretary.route("add_secretary/<company_id>", methods=["POST", "GET"])
def add_secretary(company_id):
    form = SecretaryInfo()

    if form.validate_on_submit():
        capacity = ""
        capacity1 = form.corporate.data
        capacity2 = form.naturalPerson.data
        if capacity1 is None and capacity2 is not None:
            capacity = capacity2
        elif capacity2 is None and capacity1 is not None:
            capacity = capacity1

        newSecretary = Secretary(companyOrPerson=capacity, nameInChinese=form.nameInChinese.data,
                                 englishGivenName=form.englishGivenName.data, englishName=form.englishName.data,
                                 previousChineseName=form.previousChineseName.data, previousEnglishName=form.previousEnglishName.data,
                                 chineseAliasName=form.chineseAliasName.data, englishAliasName=form.englishAliasName.data,
                                 companyNumber=form.companyNumber.data, hkIDcardNumber=form.hkIDcardNumber.data,
                                 passportIssuedCountry=form.passportIssuedCountry.data, passportNumber=form.passportNumber.data,
                                 company_id=company_id)
        db.session.add(newSecretary)
        db.session.commit()

        return redirect(url_for('fillingForm.edit_company_info', company_id=company_id))

    return render_template('changeSecretary/newSecretary.html', form=form)