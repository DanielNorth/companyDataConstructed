from flask_login import UserMixin
from flask import current_app
from flask_login import UserMixin
from companyFilling import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    companies = db.relationship('Company', backref='owner', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return self.username, self.email


class Company(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(200))

    # The owner username of this company
    # this is a many in the table
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # this is a one in the table
    # one company can have many form
    nar1form = db.relationship('Nar1data', backref='company_file', lazy=True)

    def __str__(self):
        return self.companyName, self.owner_id


class Nar1data(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # the company that owns the form
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    companyName = db.Column(db.String(200))
    businessName = db.Column(db.String(200))
    typeOfCompany = db.Column(db.String(200))

    date1 = db.Column(db.String(200))
    financialStatementStartDate = db.Column(db.String(200))
    financialStatementEndDate = db.Column(db.String(200))

    registeredOfficeAddress = db.Column(db.Text())
    emailAddress = db.Column(db.String(200))
    mortgagesCharges = db.Column(db.Text())
    q9 = db.Column(db.String(100))

    def __str__(self):
        return self.companyName, self.typeOfCompany



