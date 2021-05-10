from flask import render_template, url_for, flash, redirect, send_file, Blueprint, abort, request
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import Company, Nar1data, Director, TestDB
from companyFilling import db
from companyFilling.changeDirector.forms import DirectorInfo, Test, DirectorInfo1
import os
import uuid

changeDirector = Blueprint('changeDirector', __name__)


@changeDirector.route('add_director/<company_id>', methods=['GET', "POST"])
@login_required
def add_director(company_id):
    company = Company.query.filter_by(id=company_id).first()
    if company.owner_id != current_user.id:
        abort(403)

    form = DirectorInfo()
    if form.validate_on_submit():
        # if request.form.get("reason") == "AlternateDirector":
        #     alternateToWho = request.form.get('alternateTo')

        newDirector = Director(company_id=company_id, directorNameInChinese=form.directorNameInChinese.data,
                               directorSurname=form.directorSurname.data, directorOtherName=form.directorOtherName.data,
                               hkidCardNumber=form.hkidCardNumber.data,
                               directorEmail=form.directorEmail.data, passportIssuingCountry=form.passportIssuingCountry.data,
                               passportNumber=form.passportNumber.data, companyOwnerID=current_user.id,
                               companyOrPerson="Natural Person", capacity=request.form.get("reason"),
                               alternateTo=request.form.get('alternateTo')
                               )

        db.session.add(newDirector)
        db.session.commit()

        from datetime import datetime
        now = datetime.now()
        message = f"""Date add: {now.strftime("%d %B, %Y")}
Director English Name: {form.directorOtherName.data} {form.directorSurname.data}
Director Chinese Name: {form.directorNameInChinese.data}
Director Email: {form.directorEmail.data}
"""
        with open(f"companyFilling/companyDirectorChangeLog/{company_id}.txt", 'a') as file:
            file.write(message)
            file.write('\n')

        return redirect(url_for('fillingForm.edit_company_info', company_id=company_id))

    return render_template("changeDirector/addDirector.html", form=form)


@changeDirector.route('add_director_corp/<company_id>', methods=['GET', "POST"])
@login_required
def add_director_corp(company_id):
    company = Company.query.filter_by(id=company_id).first()
    if company.owner_id != current_user.id:
        abort(403)

    form = DirectorInfo()
    if form.validate_on_submit():
        newDirector = Director(company_id=company_id, directorNameInChinese=form.directorNameInChinese.data,
                               directorOtherName=form.directorOtherName.data, directorEmail=form.directorEmail.data,
                               companyOwnerID=current_user.id, companyOrPerson="Corporate", capacity=request.form.get("reason"),
                               alternateTo=request.form.get('alternateTo'), companyNumber=form.companyNumber.data
                               )

        db.session.add(newDirector)
        db.session.commit()

        from datetime import datetime
        now = datetime.now()
        message = f"""Date add: {now.strftime("%d %B, %Y")}
        Director English Name: {form.directorOtherName.data} 
        Director Chinese Name: {form.directorNameInChinese.data}
        Director Email: {form.directorEmail.data}
        """
        with open(f"companyFilling/companyDirectorChangeLog/{company_id}.txt", 'a') as file:
            file.write(message)
            file.write('\n')

        return redirect(url_for('fillingForm.edit_company_info', company_id=company_id))

    return render_template("changeDirector/addDirectorCorp.html", form=form)



@changeDirector.route('remove_director/<company_id>', methods=['GET', "POST"])
@login_required
def remove_director(company_id):
    directors = Director.query.filter_by(company_id=company_id)

    director = Director.query.filter_by(company_id=company_id).first()
    if current_user.id != director.companyOwnerID:
        abort(403)

    uuidKey = uuid.uuid4()
    return render_template("changeDirector/removeDirector.html", directors=directors, uuidKey=uuidKey)


@changeDirector.route("remove/<uuid><director_id>")
@login_required
def resign(director_id, uuid):
    director = Director.query.filter_by(id=director_id).first()

    if director.companyOwnerID != current_user.id:
        abort(403)

    from datetime import datetime
    now = datetime.now()
    message = f"""Date resign: {now.strftime("%d %B, %Y")}
Director English Name: {director.directorNameInEnglish}
Director Chinese Name: {director.directorNameInChinese}
Director Email: {director.directorEmail}
"""
    company = Director.query.filter_by(company_id=director.company_id).first()

    if director.companyOrPerson == "Natural Person":
        xml = f"""<Eform xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="CR-Format.xsd" id="ND4">
    <TextField id="language">E</TextField>
    <TextField id="hiddenCompNo">{company.companyNumber}</TextField>
    <TextField id="compName">{company.companyName} </TextField>
    <TextField id="S2CapacityGroup1">false</TextField>
    <TextField id="S2CapacityGroup2">true</TextField>
    <TextField id="S2CapacityGroup3">false</TextField>
    <TextField id="S2alternateTo"/>
    <TextField id="S2chnName">{director.directorNameInChinese}</TextField>
    <TextField id="S2engSurname">{director.directorSurname}</TextField>
    <TextField id="S2engOthName">{director.directorOtherName}</TextField>
    <TextField id="S2HKID">{director.hkidCardNumber}</TextField>
    <TextField id="S2PPTNo">{director.passportNumber}</TextField>
    <TextField id="S2corpChnName"/>
    <TextField id="S2corpEngName"/>
    <TextField id="S2ResignDate">20131018</TextField>
    <TextField id="S2cessContGroup">S2cessContGroup2</TextField>
    <TextField id="S2corpCompNo"/>
    <TextField id="S3regNoticeGroup">S3regNoticeGroup1</TextField>
    <TextField id="nameCRNo">{director.directorNameInChinese}##{director.directorSurname}, {director.directorOtherName}##</TextField>
    <TextField id="signatoryCRNo"/>
    <TextField id="nameCapacity">{director.directorNameInChinese}##{director.directorSurname}, {director.directorOtherName}##D</TextField>
    <TextField id="signCapacity">{director.cap}</TextField>
    <TextField id="signName">{director.directorSurname}, {director.directorOtherName}</TextField>
    <TextField id="signDate">20131018</TextField>
    </Eform>
        """
    elif director.companyOrPerson == "Corporate":
        xml = f"""
        """



    with open(f"companyFilling/companyDirectorChangeLog/{director.company_id}.txt", 'a') as file:
        file.write(message)
        file.write('\n')

    Director.query.filter_by(id=director_id).delete()
    db.session.commit()

    return redirect(url_for("fillingForm.edit_company_info"))


@changeDirector.route("remove/form/<director_id>")
@login_required
def remove_director_form(director_id):
    pass


@changeDirector.route("director/all_director/<uuid><company_id>")
@login_required
def show_all_director(uuid, company_id):
    return render_template("changeDirector/listAllDirector.html")


@changeDirector.route("director/all_director/a", methods=['GET', "POST"])
@login_required
def check():
    form = Test()
    if form.validate_on_submit():
        if request.form.get("reason") == "":
            otherCompany = request.form.get('other_reason')
        else:
            otherCompany = request.form.get("reason")

        theCompany = TestDB(otherCompany=otherCompany)
        db.session.add(theCompany)
        db.session.commit()

    return render_template("testing/checkBox_selectField.html", form=form)

