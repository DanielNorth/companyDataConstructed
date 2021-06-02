from flask import render_template, url_for, flash, redirect, send_file, Blueprint, abort, request
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import Company, Nar1data, Director, TestDB, DirectorChangeResolution
from companyFilling import db
from companyFilling.changeDirector.forms import DirectorInfo, Test
import os
import uuid
from datetime import date

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
    directors = Director.query.filter_by(company_id=boardRes.company_id).all()
    return render_template("allDocuments/DirectorChangeBoardRes/changeDirectorRes.html", info=boardRes,
                                                                                         directors=directors)


@allDocuments.route("send_to_directors/<company_id><uuid>")
@login_required
def send_to_directors(company_id, uuid):
    directors = Director.query.filter_by(company_id=company_id).all()
    allEmail = [i.directorEmail for i in directors]


class Pdf():
    def render_pdf(self, html):
        from xhtml2pdf import pisa
        from io import StringIO

        pdf = StringIO()

        pisa.CreatePDF(StringIO(html), pdf)

        return pdf.getvalue()

import pdfkit
from flask import make_response

@allDocuments.route('Board_resolution/director_change_pdf/<uuid>',  methods=['GET'])
def view_board_resolution(uuid):
    boardRes = DirectorChangeResolution.query.filter_by(uuid=uuid).first()
    directors = Director.query.filter_by(company_id=boardRes.company_id).all()

    path_wkhtmltopdf = "D:\website_research\wkhtmltopdf\\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    html = render_template('allDocuments/DirectorChangeBoardRes/changeDirectorRes.html', info=boardRes, directors=directors)
    pdf = pdfkit.from_string(html, False, configuration=config)
    response = make_response(pdf)

    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response
