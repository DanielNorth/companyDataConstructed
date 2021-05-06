from flask import render_template, url_for, flash, redirect, send_file, Blueprint, abort, request
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import Company, Nar1data, Director
from companyFilling import db
from companyFilling.changeDirector.forms import DirectorInfo
import os

companySecretary = Blueprint("companySecretary", __name__)


@companySecretary.route("change_secretary", methods=["POST", "GET"])
@login_required
def change_secretary():
    return render_template("changeSecretary/newSecretary.html")
