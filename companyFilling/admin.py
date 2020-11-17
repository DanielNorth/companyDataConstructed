from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from companyFilling.model import User, db
from flask import Blueprint
from flask import current_app

# admin = Blueprint('admin', __name__)
#
#
# class MyModelView(ModelView):
#     def is_accessible(self):
#         return True
#
#
# # admins = Admin(app)
# # admins.add_view(ModelView(User, db.session))
# #
# @admin.route('/')
# def adminView():
#     admins = Admin(app=current_app)
#     admins.add_view(ModelView(User, db.session))