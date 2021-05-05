from flask import render_template, url_for, flash, redirect, send_file, Blueprint, abort, request
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import Company, Nar1data, Director
from companyFilling import db
from companyFilling.changeDirector.forms import DirectorInfo
import os

changeDirector = Blueprint('changeDirector', __name__)


@changeDirector.route('add_director/<company_id>', methods=['GET', "POST"])
@login_required
def add_director(company_id):
    form = DirectorInfo()

    if form.validate_on_submit():
        newDirector = Director(company_id=company_id, directorNameInChinese=form.directorNameInChinese.data,
                               directorNameInEnglish=form.directorNameInEnglish.data,
                               hkidCardNumber=form.hkidCardNumber.data,
                               directorEmail=form.directorEmail.data, passportIssuingCountry=form.passportIssuingCountry.data,
                               passportNumber=form.passportNumber.data)

        db.session.add(newDirector)
        db.session.commit()

        from datetime import datetime
        now = datetime.now()
        message = f"""Date add: {now.strftime("%d %B, %Y")}
Director English Name: {form.directorNameInEnglish.data}
Director Chinese Name: {form.directorNameInChinese.data}
Director Email: {form.directorEmail.data}
"""
        with open(f"companyFilling/companyDirectorLog/{company_id}.txt", 'a') as file:
            file.write(message)
            file.write('\n')

        return redirect(url_for('fillingForm.home'))

    return render_template("addDirector.html", form=form)


@changeDirector.route('remove_director/<company_id>', methods=['GET', "POST"])
@login_required
def remove_director(company_id):
    directors = Director.query.filter_by(company_id=company_id)

    director = Director.query.filter_by(company_id=company_id).first()
    if current_user.id != director.company_id:
        abort(403)

    return render_template("removeDirector.html", directors=directors)


@changeDirector.route("remove/<director_id>")
@login_required
def remove(director_id):
    director = Director.query.filter_by(id=director_id).first()

    if current_user.id != director.company_id:
        abort(403)

    from datetime import datetime
    now = datetime.now()
    message = f"""Date removed: {now.strftime("%d %B, %Y")}
Director English Name: {director.directorNameInEnglish}
Director Chinese Name: {director.directorNameInChinese}
Director Email: {director.directorEmail}
"""

    with open(f"companyFilling/companyDirectorLog/{director.company_id}.txt", 'a') as file:
        file.write(message)
        file.write('\n')

    Director.query.filter_by(id=director_id).delete()
    db.session.commit()

    return redirect(url_for("fillingForm.home"))
