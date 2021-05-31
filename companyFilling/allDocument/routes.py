from flask import render_template, url_for, flash, redirect, send_file, Blueprint, abort, request
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import Company, Nar1data, Director, TestDB
from companyFilling import db
from companyFilling.changeDirector.forms import DirectorInfo, Test
import os
import uuid
from datetime import date

allDocuments = Blueprint('allDocuments', __name__)


@allDocuments.route("all/<company_id>")
@login_required
def all(company_id):
    directors = Director.query.filter_by(company_id=company_id).count()
    return render_template('allDocuments/show_all.html', all_directors=directors)
