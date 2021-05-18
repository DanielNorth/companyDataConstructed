from flask import render_template, url_for, flash, redirect, send_file, Blueprint, abort, request
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import Company, Nar1data, Director
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

    #return render_template("changeSecretary/newSecretary.html", form=form)
    return render_template('changeSecretary/newSecretary.html', form=form)