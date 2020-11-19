from flask import render_template, Blueprint

homePage = Blueprint('homePage', __name__)


@homePage.route('/')
def homepage():
    return render_template('homePage.html')