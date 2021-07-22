from flask import render_template, url_for, flash, redirect, send_file, Blueprint, abort, request
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import UserMessage, Company, Director, ShareHolderStake, ShareCapital, User
from companyFilling import db
from companyFilling.changeDirector.forms import Test
import os
import uuid
from datetime import date
from .forms import CompanyInfo, SubmitButton
import stripe

incorporate_new_company = Blueprint('incorporate_new_company', __name__)


@incorporate_new_company.route("", methods=["POST", "GET"])
@login_required
def new_company():
    form = CompanyInfo()

    if request.method == "POST":
        newCompany = Company(companyName=form.companyName.data, companyChineseName=form.companyChineseName.data,
                             companyEmail=form.companyEmail.data, businessName=form.businessName.data,
                             addressOfRegisteredOffice1=form.addressOfRegisteredOffice1.data,
                             addressOfRegisteredOffice2=form.addressOfRegisteredOffice2.data,
                             addressOfRegisteredOffice3=form.addressOfRegisteredOffice3.data,
                             owner_id=current_user.id, plan='starter')
        db.session.add(newCompany)
        db.session.commit()

        newShareCaptial = ShareCapital(company_id=newCompany.id, shareClass="ordinary",
                                       currency=form.currency.data, totalNumber=form.shares_issued.data,
                                       totalAmount=form.totalAmount.data, totalPaidUp=form.totalPaidUp.data)
        db.session.add(newShareCaptial)
        db.session.commit()

        return redirect(url_for('incorporate_new_company.add_person', company_id=newCompany.id, total_shares=form.shares_issued.data,
                                pageNumber=1))

    return render_template('newCompany/multi-step-form.html', form=form)


@incorporate_new_company.route("directors_founders/<company_id>/<total_shares>", methods=["POST", "GET"])
@login_required
def add_person(company_id, total_shares):
    try:
        share_holders = ShareHolderStake.query.filter_by(company_id=company_id).all()
    except:
        share_holders = None

    if request.method == "POST":
        return redirect(url_for("incorporate_new_company.review", company_id=company_id))

    return render_template("newCompany/multi-step-form2.html", company_id=company_id, total_shares=total_shares,
                                                               share_holders=share_holders)


@incorporate_new_company.route('add_director/<company_id>/<total_shares>', methods=['GET', "POST"])
@login_required
def add_director(company_id, total_shares):
    company = Company.query.filter_by(id=company_id).first()
    if company.owner_id != current_user.id:
        abort(403)

    from .forms import DirectorInfo

    form = DirectorInfo()
    if form.validate_on_submit():
        # if request.form.get("reason") == "AlternateDirector":
        #     alternateToWho = request.form.get('alternateTo')
        today = date.today()

        newDirector = Director(company_id=company_id, directorNameInChinese=form.directorNameInChinese.data,
                               directorSurname=form.directorSurname.data, directorOtherName=form.directorOtherName.data,
                               hkidCardNumber=form.hkidCardNumber.data,
                               directorEmail=form.directorEmail.data, passportIssuingCountry=form.passportIssuingCountry.data,
                               passportNumber=form.passportNumber.data, companyOwnerID=current_user.id,
                               companyOrPerson="Natural Person", capacity=request.form.get("reason"),
                               alternateTo=request.form.get('alternateTo'), address1=form.address1.data,
                               address2=form.address2.data, address3=form.address3.data,
                               dateAdded=today.strftime("%B %d, %Y"), active="active")

        db.session.add(newDirector)
        db.session.commit()

        return redirect(url_for('incorporate_new_company.add_person', company_id=company_id, total_shares=total_shares))

    return render_template("changeDirector/addDirector.html", form=form)


@incorporate_new_company.route('add_director_corp/<company_id>/<total_shares>', methods=['GET', "POST"])
@login_required
def add_director_corp(company_id, total_shares):
    company = Company.query.filter_by(id=company_id).first()
    if company.owner_id != current_user.id:
        abort(403)

    from .forms import DirectorInfo

    form = DirectorInfo()
    if form.validate_on_submit():
        today = date.today()
        newDirector = Director(company_id=company_id, directorNameInChinese=form.directorNameInChinese.data,
                               directorOtherName=form.englishName.data, directorEmail=form.directorEmail.data,
                               companyOwnerID=current_user.id, companyOrPerson="Corporate",
                               capacity=request.form.get("reason"),
                               alternateTo=request.form.get('alternateTo'), companyNumber=form.companyNumber.data,
                               address1=form.address1.data, address2=form.address2.data,
                               address3=form.address3.data, dateAdded=today.strftime("%B %d, %Y"),
                               active="active", directorSurname=""
                               )

        db.session.add(newDirector)
        db.session.commit()

        return redirect(url_for('incorporate_new_company.add_person', company_id=company_id, total_shares=total_shares))

    return render_template("changeDirector/addDirectorCorp.html", form=form)


@incorporate_new_company.route("add_existing_shareholder/<company_id>/<total_shares>", methods=["POST", "GET"])
@login_required
def add_existing_shareholder(company_id, total_shares):
    company = Company.query.filter_by(id=company_id).first()
    if company.owner_id != current_user.id:
        abort(403)
    from companyFilling.shareHolder.forms import ShareInfo
    from companyFilling.model import ShareCapital

    form = ShareInfo()
    try:
        share_clas = ShareCapital.query.filter_by(company_id=company_id).all()
        share_classes = []
        for i in share_clas:
            if i.shareClass not in share_classes:
                share_classes.append(i.shareClass)
    except:
        share_classes = []

    if form.validate_on_submit():
        if request.form.get("shareOfClass") == "":
            shareClass = str(request.form.get('other_class'))
        else:
            shareClass = str(request.form.get("shareOfClass"))

        existingShareHolder = ShareHolderStake(name=form.name.data, shareClass=' '.join(shareClass.split()),
                                               totalShares=form.totalShares.data, address=form.address.data,
                                               company_id=company_id, email=form.email.data)
        db.session.add(existingShareHolder)
        db.session.commit()
        return redirect(url_for("incorporate_new_company.add_person", company_id=company_id, total_shares=total_shares))

    return render_template('newCompany/addExistingShareHolder.html', company_id=company_id, form=form, share_classes=share_classes,
                           total_shares=total_shares)


@incorporate_new_company.route("review/<company_id>", methods=["POST", "GET"])
@login_required
def review(company_id):
    company = Company.query.filter_by(id=company_id).first()
    if company.owner_id != current_user.id:
        abort(403)

    shareHolders = ShareHolderStake.query.filter_by(company_id=company_id).all()
    directors = Director.query.filter_by(company_id=company_id).all()

    # if request.method == "POST":
    #     return redirect(url_for('incorporate_new_company.checkout'))

    return render_template('newCompany/review.html', company=company, share_holders=shareHolders,
                           directors=directors, company_id=company_id, key=os.environ.get("stripe_public_key"))


@incorporate_new_company.route("edit/<shareHolder_id>/<company_id>", methods=["POST", "GET"])
@login_required
def edit_shareholder(shareHolder_id, company_id):
    try:
        share_clas = ShareHolderStake.query.filter_by(company_id=company_id).all()
        share_classes = []
        for i in share_clas:
            if i.shareClass not in share_classes:
                share_classes.append(i.shareClass)
    except:
        share_classes = []
    shareHolderInfo = ShareHolderStake.query.filter_by(id=shareHolder_id).first()

    from companyFilling.shareHolder.forms import ShareInfo
    form = ShareInfo(obj=shareHolderInfo)

    if form.validate_on_submit():
        obj = ShareHolderStake.query.filter_by(id=shareHolder_id).first()
        obj.name = form.name.data
        obj.address = form.address.data
        obj.shareClass = form.shareClass.data
        obj.totalShares = form.totalShares.data
        db.session.commit()
        return redirect(url_for("incorporate_new_company.review", company_id=company_id))

    return render_template("shareHolder/editShareHolder.html", id=shareHolder_id, form=form, share_classes=share_classes)


@incorporate_new_company.route("director/editInfo/<director_id>", methods=["POST", 'GET'])
@login_required
def edit_director(director_id):
    director = Director.query.filter_by(id=director_id).first()
    if director.companyOwnerID != current_user.id:
        abort(403)

    from companyFilling.changeDirector.forms import DirectorInfo

    director = Director.query.filter_by(id=director_id).first()
    company_id = director.company_id

    if director.companyOrPerson == "Natural Person":
        form = DirectorInfo(obj=director)

        if form.validate_on_submit():
            director.directorNameInChinese = form.directorNameInChinese.data
            director.directorOtherName = form.directorOtherName.data
            director.directorSurname=form.directorSurname.data
            director.directorEmail = form.directorEmail.data
            director.companyNumber = form.companyNumber.data
            director.alternateTo = request.form.get('alternateTo')
            director.address1 = form.address1.data
            director.address2 = form.address2.data
            director.address3 = form.address3.data
            director.hkidCardNumber = form.hkidCardNumber.data
            director.passportIssuingCountry = form.passportIssuingCountry.data
            director.passportNumber = form.passportNumber.data

            db.session.commit()
            return redirect(url_for("fillingForm.edit_company_info", company_id=company_id))

        return render_template("changeDirector/addDirector.html", form=form)

    elif director.companyOrPerson == "Corporate":
        form = DirectorInfo(obj=director)

        if form.validate_on_submit():
            director.directorNameInChinese = form.directorNameInChinese.data
            director.directorOtherName = form.englishName.data
            director.directorEmail = form.directorEmail.data
            director.companyNumber=form.companyNumber.data
            director.alternateTo = request.form.get('alternateTo')
            director.address1 = form.address1.data
            director.address2 = form.address2.data
            director.address3 = form.address3.data

            db.session.commit()
            return redirect(url_for("incorporate_new_company.review"))

        return render_template("changeDirector/addDirectorCorp.html", form=form)


@incorporate_new_company.route("checkout")
@login_required
def checkout():
    import stripe
    secret_key = os.environ.get("stripe_secret_key")
    stripe.api_key = secret_key

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1JFNngBV8igYyrszd4X24ogc',
            'quantity': 1,
        }],
        mode='subscription',
        success_url=url_for("incorporate_new_company.success_payment", _external=True),
        cancel_url=url_for("incorporate_new_company.payment_fail", _external=True)
    )
    return {
        'checkout_session_id': session['id'],
        'checkout_public_key': "pk_live_51InDYVBV8igYyrsz8ZRAHjyDQfnnSvS1AVv4BTN6iHdTw41pWOXw86yGxzEXBiKcVLVh3uZWrOPA6qQtpssY11HG00jReZIM6z"
    }


@incorporate_new_company.route('/stripe_webhook', methods=['POST'])
@login_required
def stripe_webhook():
    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = os.environ.get("stripe_endpoint_secret")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)

    return {}


@incorporate_new_company.route("success_payment")
@login_required
def success_payment():
    from flask_mail import Message
    from companyFilling import mail

    msg = Message(f'New company registration request, user_id: {current_user.id}',
                  sender='daniel@hspector.com',
                  recipients=['asz24687@gmail.com'])
    msg.body = ""
    mail.send(msg)

    newMessage = UserMessage(user_id=current_user.id, message="Your request to file company is already is processed")
    db.session.add(newMessage)
    db.session.commit()

    return render_template('newCompany/success_payment.html')


@incorporate_new_company.route("payment_fail")
@login_required
def payment_fail():
    return render_template("newCompany/fail_payment.html")


@incorporate_new_company.route("new_shareHolder/<company_id>", methods=["POST", "GET"])
@login_required
def insert_shareHolder(company_id):
    from flask import jsonify

    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        totalShares = request.form['totalShares']

        newShareHolder = ShareHolderStake(name=name, address=address,
                                          email=email, shareClass="ordinary",
                                          totalShares=int(totalShares), company_id=int(company_id))
        db.session.add(newShareHolder)
        db.session.commit()
    return jsonify("success")