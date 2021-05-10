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
    username = db.Column(db.String(20))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    ownedCompany = db.Column(db.Integer)

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
    businessName = db.Column(db.String(200), nullable=True)
    companyNumber = db.Column(db.String(20), nullable=True)
    typeOfCompany = db.Column(db.String(100))
    addressOfRegisteredOffice1 = db.Column(db.String(100), nullable=True)
    addressOfRegisteredOffice2 = db.Column(db.String(100), nullable=True)
    addressOfRegisteredOffice3 = db.Column(db.String(100), nullable=True)
    addressOfRegisteredOfficeRegion = db.Column(db.String(30), nullable=True)
    companyEmail = db.Column(db.String(100), nullable=True)
    nonShareHolder = db.Column(db.Integer, nullable=True)
    shares_issued = db.Column(db.Integer, nullable=True)

    # The owner username of this company
    # this is a many in the table
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # this is a one in the table
    # one company can have many form
    nar1form = db.relationship('Nar1data', backref='company_file', lazy=True)

    # one to one to the director model

    def __str__(self):
        return self.companyName, self.owner_id


class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    directorNameInChinese = db.Column(db.String(100), nullable=False)
    directorSurname = db.Column(db.String(50), nullable=True)
    directorOtherName = db.Column(db.String(100), nullable=True)
    capacity = db.Column(db.String(50), nullable=False)

    alternateTo = db.Column(db.String(200), nullable=True)

    previousChineseName = db.Column(db.String(100), nullable=True)
    previousEnglishName = db.Column(db.String(200), nullable=True)
    chineseAlias = db.Column(db.String(100), nullable=True)
    englishAlias = db.Column(db.String(200), nullable=True)
    companyOrPerson = db.Column(db.String(50), nullable=True)

    companyNumber = db.Column(db.String(30), nullable=True)

    hkidCardNumber = db.Column(db.String(200), nullable=True)
    directorEmail = db.Column(db.String(200), nullable=True)
    passportIssuingCountry = db.Column(db.String(200), nullable=True)
    passportNumber = db.Column(db.String(200), nullable=True)

    companyOwnerID = db.Column(db.Integer)
    company = db.relationship("Company", backref=db.backref('directors', lazy='dynamic', collection_class=list))


class Secretary(db.Model):
    __tablename__ = "secretaries"

    id = db.Column(db.Integer, primary_key=True)
    nameInChinese = db.Column(db.String(100))
    englishGivenName = db.Column(db.String(60), nullable=True)
    englishName = db.Column(db.String(100), nullable=True)
    previousChineseName = db.Column(db.String(100), nullable=True)
    previousEnglishName = db.Column(db.String(200), nullable=True)
    chineseAliasName = db.Column(db.String(100), nullable=True)
    englishAliasName = db.Column(db.String(200), nullable=True)
    companyOrPerson = db.Column(db.String(100))

    hkIDcardNumber = db.Column(db.String(20), nullable=True)
    passportIssuedCountry = db.Column(db.String(100), nullable=True)
    passportNumber = db.Column(db.String(50), nullable=True)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship("Company", backref=db.backref('secretaries', lazy='dynamic', collection_class=list))


class Nar1data(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # the company that owns the form
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    companyName = db.Column(db.String(200))
    S2compName = db.Column(db.String(200))
    typeOfCompany = db.Column(db.String(200))

    date1 = db.Column(db.DateTime)
    financialStatementStartDate = db.Column(db.DateTime)
    financialStatementEndDate = db.Column(db.DateTime)

    registeredOfficeAddress = db.Column(db.Text())
    emailAddress = db.Column(db.String(200))
    mortgagesCharges = db.Column(db.Text())
    q9 = db.Column(db.String(100))

    def __repr__(self):
        return self.companyName, self.typeOfCompany


class TestDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    otherCompany = db.Column(db.String(300))


class ShareHolderStake(db.Model):
    __tablename__ = "shareholder"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(300), nullable=True)

    # holding shares in which company
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship("Company", backref=db.backref('shareholder', lazy='dynamic', collection_class=list))

    shareClass = db.Column(db.String(100), nullable=True)
    totalShares = db.Column(db.Integer, nullable=True)

    transferFrom = db.Column(db.String(50), nullable=True)
    transferFromDate = db.Column(db.String(50), nullable=True)
    transferTo = db.Column(db.String(50), nullable=True)
    transferToDate = db.Column(db.String(50), nullable=True)


class ShareTransferLog(db.Model):
    __tablename__ = 'sharetransferlog'

    id = db.Column(db.Integer, primary_key=True)

    # holding shares in which company
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship("Company", backref=db.backref('sharetransferlog', lazy='dynamic', collection_class=list))

    # the value is the shareholder id
    transferer = db.Column(db.Integer, nullable=False)
    reciver = db.Column(db.Integer, nullable=False)

    transcation_date = db.Column(db.String(100), nullable=False)
    shares_transfered = db.Column(db.Integer, nullable=False)
