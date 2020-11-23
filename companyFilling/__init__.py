from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from companyFilling.config import Config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login/'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Bootstrap(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    from companyFilling.model import User, Company, Nar1data
    with app.app_context():
       db.create_all()

    from companyFilling.users.routes import users
    app.register_blueprint(users, url_prefix='/users')

    from companyFilling.fillingForm.routes import fillingForm
    app.register_blueprint(fillingForm, url_prefix='/home')
    #app.register_blueprint(fillingForm, url_prefix=f'/{current_user.username}')

    from companyFilling.homePage import homePage
    app.register_blueprint(homePage, url_prefix='/')


    from flask_admin.contrib.sqla import ModelView
    from flask_admin import Admin
    admins = Admin(app)
    admins.add_view(ModelView(User, db.session))
    admins.add_view((ModelView(Company, db.session)))
    admins.add_view(ModelView(Nar1data, db.session))


    return app

