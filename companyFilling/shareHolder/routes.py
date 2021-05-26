from flask import render_template, url_for, flash, redirect, send_file, Blueprint, abort, request
from flask_login import login_user, current_user, logout_user, login_required
from companyFilling.model import Company, User, Nar1data, ShareHolderStake
from companyFilling import db
from companyFilling.fillingForm.forms import Nar1Form, AddCompany, aButton, CompanyInfo
from companyFilling.shareHolder.forms import ShareInfo, ShareCapitalForm


shareHolder = Blueprint('shareHolder', __name__)


@shareHolder.route("add_existing_shareholder/<hash><company_id>", methods=["POST", "GET"])
@login_required
def add_existing_shareholder(hash, company_id):
    form = ShareInfo()
    try:
        share_clas = ShareHolderStake.query.filter_by(company_id=company_id).all()
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
                                               company_id=company_id)
        db.session.add(existingShareHolder)
        db.session.commit()
        return redirect(url_for("fillingForm.edit_company_info", company_id=company_id))

    return render_template('shareHolder/addExistingShareHolder.html', company_id=company_id, form=form, share_classes=share_classes)


@shareHolder.route("all_share_holder/<company_id>")
@login_required
def show_shareholder(company_id):
    shareHolders = ShareHolderStake.query.filter_by(company_id=company_id).all()
    return render_template("shareHolder/showAllShareholder.html", shareHolders=shareHolders, company_id=company_id)


@shareHolder.route("edit/<shareHolder_id>/<company_id>", methods=["POST", "GET"])
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

    form = ShareInfo(obj=shareHolderInfo)

    if form.validate_on_submit():
        obj = ShareHolderStake.query.filter_by(id=shareHolder_id).first()
        obj.name = form.name.data
        obj.address = form.address.data
        obj.shareClass = form.shareClass.data
        obj.totalShares = form.totalShares.data
        db.session.commit()
        return redirect(url_for("fillingForm.edit_company_info", company_id=company_id))

    return render_template("shareHolder/editShareHolder.html", id=shareHolder_id, form=form, share_classes=share_classes)


@shareHolder.route("transfer/<shareHolder_id>", methods=["POST", "GET"])
@login_required
def transfer_share(shareHolder_id):
    return render_template("shareHolder/transferShare")


@shareHolder.route("share_capital/<company_id>", methods=["POST", "GET"])
@login_required
def share_capital(company_id):
    try:
        share_clas = ShareHolderStake.query.filter_by(company_id=company_id).all()
        share_classes = []
        for i in share_clas:
            if i.shareClass not in share_classes:
                share_classes.append(i.shareClass)
    except:
        share_classes = []
    share_classes1 = [i.replace(" ", "_") for i in share_classes]

    return render_template('shareHolder/shareCapital.html', share_classes=share_classes1, company_id=company_id)


@shareHolder.route("edit_share_capital/addInfo/<company_id>/<share_class>", methods=["POST", "GET"])
@login_required
def edit_share_capital(company_id, share_class):
    shareClass = share_class.replace("_"," ")

    shareClassRow = ShareHolderStake.query.filter_by(company_id=company_id, shareClass=shareClass).all()

    totalClassShare = 0
    for i in shareClassRow:
        totalClassShare += i.totalShares

    # try:
    #     share_clas = ShareHolderStake.query.filter_by(company_id=company_id).all()
    #     share_classes = []
    #     for i in share_clas:
    #         if i.shareClass not in share_classes:
    #             share_classes.append(i.shareClass)
    # except:
    #     share_classes = []

    return render_template('shareHolder/addShareCapital.html', share_classes=shareClass, company_id=company_id,
                                                               total_share=totalClassShare)



