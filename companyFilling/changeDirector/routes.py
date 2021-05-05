from flask import render_template, url_for, flash, redirect, send_file, Blueprint, abort, request
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import Company, Nar1data
from companyFilling import db
from companyFilling.changeDirector.forms import DirectorInfo
import os

changeDirector = Blueprint('changeDirector', __name__)


@changeDirector.route('add_director/<company_id>')
@login_required
def add_director(company_id):
    form = DirectorInfo()
    return render_template("", form=form)
    pass
