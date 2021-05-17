from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from companyFilling.users.forms import RegisterForm, LoginForm, ResetPasswordForm, NewPassword
from companyFilling.model import User, Company, Director, ShareHolderStake
from companyFilling import db, mail
from companyFilling.users.utils import send_reset_email
import datetime
from .utils import count_all_shares

fileNar1 = Blueprint("fileNar1", __name__)


@fileNar1.route("<company_num>")
@login_required
def file(company_num):
    company = Company.query.filter_by(id=company_num).first()
    directors = Director.query.filter_by(company_id=company_num).all()
    now = datetime.datetime.now()

    copmanyInfo = f"""<TextField id="language">E</TextField>
<TextField id="hiddenCompNo">{company.companyNumber}</TextField>
<TextField id="compName">{company.companyName} {company.companyChineseName}</TextField>
<TextField id="S2compName">{company.businessName}</TextField>
<TextField id="S3compTypeGrp">S3compTypeGrp1</TextField>
<TextField id="S4returnDate">{now.strftime("%Y%m%d")}</TextField>
<TextField id="S6addr1">{company.addressOfRegisteredOffice1}</TextField>
<TextField id="S6addr2">{company.addressOfRegisteredOffice2}</TextField>
<TextField id="S6addr3">{company.addressOfRegisteredOffice3}</TextField>
<TextField id="S6addrCountry">Hong Kong</TextField>
<TextField id="S7email">{company.companyEmail}</TextField>
<TextField id="S8mortgagesNCharges"/>
    """

    sharesInfo = ""

    shares = [i.shareClass for i in ShareHolderStake.query.filter_by(company_id=company_num).all()]
    allShareClass = []
    for i in shares:
        if i not in allShareClass:
            allShareClass.append(i)

    for i in range(len(allShareClass)):
        sharesRow = 0
        if i != 0:
            sharesInfo += "</TableField>"

        total = count_all_shares(ShareHolderStake.query.filter_by(shareClass=allShareClass[i], company_id=company_num).all())
        sharesInfo += f"""<TextField id="Sch1ReturnDate[{i}]">{now.strftime("%Y%m%d")}</TextField>
                            <TextField id="Sch1class[{i}]">{allShareClass[i]}</TextField>
                            <TextField id="Sch1totalShares[{i}]">{total}</TextField>
                            <TableField id="Sch1allotteeTab[{i}]">\n"""

        for shareHolder in ShareHolderStake.query.filter_by(shareClass=allShareClass[i], company_id=company_num).all():
            sharesInfo += f"""<Row>
                                <Column id="Sch1allotteeTab[{sharesRow}][0]">{shareHolder.name}</Column>
                                <Column id="Sch1allotteeTab[{sharesRow}][1]">{shareHolder.address}</Column>
                                <Column id="Sch1allotteeTab[{sharesRow}][2]">{shareHolder.totalShares}</Column>
                                <Column id="Sch1allotteeTab[{sharesRow}][3]"/>
                                <Column id="Sch1allotteeTab[{sharesRow}][4]"/>
                                <Column id="Sch1allotteeTab[{sharesRow}][5]"/>
                            </Row>\n"""
            sharesRow += 1

    sharesInfo += "</TableField>"


    directorInfo = ""

    directorCount = 0
    for i in directors:
        if i.capacity == "Director" and i.companyOrPerson == "Natural Person":
            message = f"""<TextField id="S12AcapacityGroup1[{directorCount}]">true</TextField>
<TextField id="S12AcapacityGroup2[{directorCount}]">false</TextField>
<TextField id="S12AalternateTo[{directorCount}]"/>
<TextField id="S12AchnName[{directorCount}]">{i.directorNameInChinese}</TextField>
<TextField id="S12AengSurname[{directorCount}]">{i.directorSurname}</TextField>
<TextField id="S12AengOthName[{directorCount}]">{i.directorOtherName}</TextField>
<TextField id="S12AchnPreName[{directorCount}]"/>
<TextField id="S12AengPreName[{directorCount}]"/>
<TextField id="S12AchnAlias[{directorCount}]"/>
<TextField id="S12AengAlias[{directorCount}]"/>
<TextField id="S12Aaddr1[{directorCount}]">Flat A, 18/F, Fortune Mansion,</TextField>
<TextField id="S12Aaddr2[{directorCount}]">1 Cheung Sha Wan Road, Kowloon</TextField>
<TextField id="S12Aaddr3[{directorCount}]"/>
<TextField id="S12AaddrCountry[{directorCount}]">Hong Kong</TextField>
<TextField id="S12Aemail[{directorCount}]">{i.directorEmail}</TextField>
<TextField id="S12AHKID[{directorCount}]">{i.hkidCardNumber[:-1]}</TextField>
<TextField id="S12AHKIDChkDig[{directorCount}]">{i.hkidCardNumber[-1]}</TextField>
<TextField id="S12ApassportCountry[{directorCount}]">{i.passportIssuingCountry}</TextField>
<TextField id="S12ApassportNo[{directorCount}]">{i.passportNumber}</TextField>\n
        """
            directorInfo += message

        elif i.capacity == "AlternateDirector" and i.companyOrPerson == "Natural Person":
            message = f"""<TextField id="S12AcapacityGroup1[{directorCount}]">false</TextField>
            <TextField id="S12AcapacityGroup2[{directorCount}]">true</TextField>
            <TextField id="S12AalternateTo[{directorCount}]">{i.alternateTo}</TextField>
            <TextField id="S12AchnName[{directorCount}]">{i.directorNameInChinese}</TextField>
            <TextField id="S12AengSurname[{directorCount}]">{i.directorSurname}</TextField>
            <TextField id="S12AengOthName[{directorCount}]">{i.directorOtherName}</TextField>
            <TextField id="S12AchnPreName[{directorCount}]"/>
            <TextField id="S12AengPreName[{directorCount}]"/>
            <TextField id="S12AchnAlias[{directorCount}]"/>
            <TextField id="S12AengAlias[{directorCount}]"/>
            <TextField id="S12Aaddr1[{directorCount}]">Flat A, 18/F, Fortune Mansion,</TextField>
            <TextField id="S12Aaddr2[{directorCount}]">1 Cheung Sha Wan Road, Kowloon</TextField>
            <TextField id="S12Aaddr3[{directorCount}]"/>
            <TextField id="S12AaddrCountry[{directorCount}]">Hong Kong</TextField>
            <TextField id="S12Aemail[{directorCount}]">{i.directorEmail}</TextField>
            <TextField id="S12AHKID[{directorCount}]">{i.hkidCardNumber[:-1]}</TextField>
            <TextField id="S12AHKIDChkDig[{directorCount}]">{i.hkidCardNumber[-1]}</TextField>
            <TextField id="S12ApassportCountry[{directorCount}]">{i.passportIssuingCountry}</TextField>
            <TextField id="S12ApassportNo[{directorCount}]">{i.passportNumber}</TextField>\n
                    """
            directorInfo += message

        directorCount += 1

    naturalPersonDirector = f"""<TextField id="S12ACount">{directorCount}</TextField>\n""" + directorInfo

    corporateDirector = """"""
    corporateDirectorCount = 0

    for i in directors:
        if i.capacity == "Director" and i.companyOrPerson == "Corporate":
            message = f"""<TextField id="S12BcapacityGroup1[{corporateDirectorCount}]">true</TextField>
                            <TextField id="S12BcapacityGroup2[{corporateDirectorCount}]">false</TextField>
                            <TextField id="S12BalternateTo[{corporateDirectorCount}]"/>
                            <TextField id="S12BchnName[{corporateDirectorCount}]">{i.directorNameInChinese}</TextField>
                            <TextField id="S12BengName[{corporateDirectorCount}]">{i.directorOtherName}</TextField>
                            <TextField id="S12Baddr1[{corporateDirectorCount}]">Room 2808-2810, 28/F,</TextField>
                            <TextField id="S12Baddr2[{corporateDirectorCount}]">Happy Commercial Building,</TextField>
                            <TextField id="S12Baddr3[{corporateDirectorCount}]">1 Queen'sway</TextField>
                            <TextField id="S12BaddrCountry[{corporateDirectorCount}]">Hong Kong</TextField>
                            <TextField id="S12Bemail[{corporateDirectorCount}]">{i.directorEmail}</TextField>
                            <TextField id="S12BcompNo[{corporateDirectorCount}]">{i.companyNumber}</TextField>\n"""
            corporateDirector += message

        elif i.capacity == "AlternateDirector" and i.companyOrPerson == "Corporate":
            message = f"""<TextField id="S12BcapacityGroup1[{corporateDirectorCount}]">false</TextField>
                            <TextField id="S12BcapacityGroup2[{corporateDirectorCount}]">true</TextField>
                            <TextField id="S12BalternateTo[{corporateDirectorCount}]">{i.alternateTo}</TextField>
                            <TextField id="S12BchnName[{corporateDirectorCount}]">{i.directorNameInChinese}</TextField>
                            <TextField id="S12BengName[{corporateDirectorCount}]">{i.directorOtherName}</TextField>
                            <TextField id="S12Baddr1[{corporateDirectorCount}]">Room 2808-2810, 28/F,</TextField>
                            <TextField id="S12Baddr2[{corporateDirectorCount}]">Happy Commercial Building,</TextField>
                            <TextField id="S12Baddr3[{corporateDirectorCount}]">1 Queen'sway</TextField>
                            <TextField id="S12BaddrCountry[{corporateDirectorCount}]">Hong Kong</TextField>
                            <TextField id="S12Bemail[{corporateDirectorCount}]">{i.directorEmail}</TextField>
                            <TextField id="S12BcompNo[{corporateDirectorCount}]">{i.companyNumber}</TextField>\n"""
            corporateDirector += message
        corporateDirectorCount += 1

    corporateDirector = f"""<TextField id="S12BCount">{corporateDirectorCount}</TextField>\n""" + corporateDirector