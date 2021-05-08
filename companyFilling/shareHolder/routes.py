from flask import render_template, url_for, flash, redirect, send_file, Blueprint, abort, request
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import Company, User, Nar1data
from companyFilling import db
from companyFilling.fillingForm.forms import Nar1Form, AddCompany, aButton, CompanyInfo
import os


shareHolder = Blueprint('shareHolder', __name__)
