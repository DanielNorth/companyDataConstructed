from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from companyFilling.config import Config
from flask_mail import Mail
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'users.login/'
login_manager.login_message_category = 'info'
mail = Mail()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Bootstrap(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app=app, db=db)

    from companyFilling.model import User, Company, ShareHolderStake, ShareCapital, Director
    with app.app_context():
       db.create_all()

    from companyFilling.users.routes import users
    app.register_blueprint(users, url_prefix='/users')

    from companyFilling.fillingForm.routes import fillingForm
    app.register_blueprint(fillingForm, url_prefix='/home')
    #app.register_blueprint(fillingForm, url_prefix=f'/{current_user.username}')

    from companyFilling.homePage import homePage
    app.register_blueprint(homePage, url_prefix='/')

    from companyFilling.changeDirector.routes import changeDirector
    app.register_blueprint(changeDirector, url_prefix='/edit_director')

    from companyFilling.companySecretary.routes import companySecretary
    app.register_blueprint(companySecretary, url_prefix='/edit_company_secretary')

    from companyFilling.shareHolder.routes import shareHolder
    app.register_blueprint(shareHolder, url_prefix='/share_holder')

    from companyFilling.fileNar1.routes import fileNar1
    app.register_blueprint(fileNar1, url_prefix='/Nar1')

    from companyFilling.allDocument.routes import allDocuments
    app.register_blueprint(allDocuments, url_prefix="/documents")

    from companyFilling.incorprate_new_company.routes import incorporate_new_company
    app.register_blueprint(incorporate_new_company, url_prefix="/incorporate_new_company")

    from flask_login import current_user

    from flask_admin.contrib.sqla import ModelView
    class CompanyModelView(ModelView):
        can_delete = True  # disable model deletion
        page_size = 50  # the number of entries to display on the list view

        def is_accessible(self):
            return int(current_user.id) == 3

        
    login_manager.login_view = 'admin.login'
    #from flask_admin.contrib.sqla import ModelView
    from flask_admin import Admin
    admins = Admin(app, name="Dashboard", url="/sitting_by_the_riverside")



    admins.add_view(CompanyModelView(User, db.session))
    admins.add_view(CompanyModelView(Company, db.session))
    admins.add_view(CompanyModelView(ShareHolderStake, db.session))
    admins.add_view(CompanyModelView(ShareCapital, db.session))
    admins.add_view(CompanyModelView(Director, db.session))

    # from companyFilling.admin import admin
    # app.register_blueprint(admin, url_prefix='/admin')

    return app