from flask import render_template, url_for, flash, redirect, send_file, Blueprint, abort, request
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import Company, Nar1data, Director, TestDB, DirectorChangeResolution
from companyFilling import db
from companyFilling.changeDirector.forms import DirectorInfo, Test
import os
import uuid
from datetime import date
from .forms import SubmitButton

allDocuments = Blueprint('allDocuments', __name__)


@allDocuments.route("DirectorChangeBoardResolution/<company_id>")
@login_required
def show_all(company_id):
    return render_template('allDocuments/show_all.html', company_id=company_id)


@allDocuments.route("all/DirectorChangeBoardResolution/<company_id>")
@login_required
def show_director_change_board_res(company_id):
    directors = DirectorChangeResolution.query.filter_by(company_id=company_id).all()
    return render_template("allDocuments/DirectorChangeBoardRes/show_all_res.html", directors=directors)


@allDocuments.route("Board_resolution/director_change/<uuid>")
def director_change_board_resolution(uuid):
    boardRes = DirectorChangeResolution.query.filter_by(uuid=uuid).first()
    directors = Director.query.filter_by(company_id=boardRes.company_id, capacity="Director").all()
    return render_template("allDocuments/DirectorChangeBoardRes/changeDirectorRes.html", info=boardRes, directors=directors,
                           uuid=uuid, one=1)


@allDocuments.route("send_to_directors/<company_id><uuid>")
@login_required
def send_to_directors(company_id, uuid):
    directors = Director.query.filter_by(company_id=company_id).all()
    allEmail = [i.directorEmail for i in directors]

    message = f"""Please head over to http://127.0.0.1:5000/documents/Board_resolution/director_change/{uuid} to
             sign the board resolution"""


import pdfkit
from flask import make_response

@allDocuments.route('Board_resolution/director_change_pdf/<uuid>',  methods=['GET'])
def view_board_resolution(uuid):
    boardRes = DirectorChangeResolution.query.filter_by(uuid=uuid).first()
    directors = Director.query.filter_by(company_id=boardRes.company_id, capacity="Director").all()

    path_wkhtmltopdf = "D:\website_research\wkhtmltopdf\\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    options = {
        "disable-local-file-access": "",
        "enable-local-file-access": None
    }

    html = render_template('allDocuments/DirectorChangeBoardRes/changeDirectorRes.html', info=boardRes, directors=directors,
                           uuid=uuid)
    pdf = pdfkit.from_string(html, False, configuration=config, options=options)
    response = make_response(pdf)

    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response


@allDocuments.route('board_resolution/director_signature/<uuid><director_id>', methods=['POST', 'GET'])
def sign_board_resolution(uuid, director_id):
    form = SubmitButton()
    director = Director.query.filter_by(id=director_id).first()

    if form.validate_on_submit():
        data_uri = request.form.get('hidden')[22:]
        print(data_uri)

        # data_uri = request.get_json().get('dataUrl')
        # data_uri = data_uri[22:]
        filename = uuid + str(director_id)

        import base64
        with open(f"companyFilling/static/img/directorSignature/{filename}.png", 'wb') as f:
            f.write(base64.b64decode(data_uri))

        return redirect(url_for('homePage.homepage'))

    return render_template('allDocuments/DirectorChangeBoardRes/sign.html', director=director, form=form)