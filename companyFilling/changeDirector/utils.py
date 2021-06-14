import os
from flask import url_for, current_app
from flask_mail import Message
from companyFilling import mail
from companyFilling.model import Company
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def send_d4_xml_email(companyName, fileLoc, subject="", body=''):
    toaddr = "asz24687@gmail.com"
    fromaddr = "danielsplash10@gmail.com"

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = f"From Company {companyName}"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "ND2A.xml"
    attachment = open(fileLoc, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'xml')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "Daniel02raptors")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


def replace_director(company_id, cessation, appointee, alreadyADirector, cessationReason, alreadyADirectorB):
    from datetime import date
    company = Company.query.filter_by(id=company_id).first()
    cessation_date = date.today()

    if alreadyADirector == "yes":
        S2AcessContG = "S2AcessContG1[0]"
    elif alreadyADirector == 'no':
        S2AcessContG = "S2AcessContG2[0]"

    if cessationReason == "Resignation/Others":
        S2AcessReasonG = "S2AcessReasonG1[0]"
    elif cessationReason == "Deceased":
        S2AcessReasonG = "S2AcessReasonG2[0]"


    xml = f"""<Eform xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="CR-Format.xsd" id="ND2A">
<TextField id="language">E</TextField>
<TextField id="hiddenCompNo">{company.companyNumber}</TextField>
<TextField id="compName">{company.companyName} {company.companyChineseName}</TextField>"""
    cessationCapacity = ["false", 'false']
    appointeeCapacity = ["false", 'false']

    if cessation.capacity == "Director":
        cessationCapacity[0] = "true"
    elif cessation.capacity == "AlternateDirector":
        cessationCapacity[1] = 'true'
    if appointee.capacity == "Director":
        appointeeCapacity[0] = 'true'
    elif appointee.capacity == "AlternateDirector":
        appointeeCapacity[1] = 'true'

    if cessation.companyOrPerson == "Natural Person":
        xml += f"""<TextField id="S2ACount">1</TextField>
        <TextField id="S2Acapacity1[0]">false</TextField>
        <TextField id="S2Acapacity2[0]">{cessationCapacity[0]}</TextField>
        <TextField id="S2Acapacity3[0]">{cessationCapacity[1]}</TextField>
        <TextField id="S2AalternateTo[0]">{cessation.alternateTo}</TextField>
        <TextField id="S2AchnName[0]">{cessation.directorNameInChinese}</TextField>
        <TextField id="S2AengSurname[0]">{cessation.directorSurname}</TextField>
        <TextField id="S2AengOthName[0]">{cessation.directorOtherName}</TextField>
        <TextField id="S2AHKID[0]">{cessation.hkidCardNumber[:-1]}({cessation.hkidCardNumber[-1]})</TextField>
        <TextField id="S2APPTNum[0]">{cessation.passportNumber}</TextField>
        <TextField id="S2AcorpSecDirNameC[0]"/>
        <TextField id="S2AcorpSecDirNameE[0]"/>
        <TextField id="S2AcessReasonG[0]">{S2AcessReasonG}</TextField>
        <TextField id="S2AcessDate[0]">{cessation_date.strftime("%Y%m%d")}</TextField>
        <TextField id="S2AcessContG[0]">{S2AcessContG}</TextField>"""

    elif cessation.companyOrPerson == "Corporate":
        xml += f"""<TextField id="S2ACount">1</TextField>
        <TextField id="S2Acapacity1[0]">false</TextField>
        <TextField id="S2Acapacity2[0]">{cessationCapacity[0]}</TextField>
        <TextField id="S2Acapacity3[0]">{cessationCapacity[1]}</TextField>
        <TextField id="S2AalternateTo[0]">{cessation.alternateTo}</TextField>
        <TextField id="S2AchnName[0]"></TextField>
        <TextField id="S2AengSurname[0]"></TextField>
        <TextField id="S2AengOthName[0]"></TextField>
        <TextField id="S2AHKID[0]"></TextField>
        <TextField id="S2APPTNum[0]"></TextField>
        <TextField id="S2AcorpSecDirNameC[0]">{cessation.directorNameInChinese}</TextField>
        <TextField id="S2AcorpSecDirNameE[0]">{cessation.directorOtherName}</TextField>
        <TextField id="S2AcessReasonG[0]">{S2AcessReasonG}</TextField>
        <TextField id="S2AcessDate[0]">{cessation_date.strftime("%Y%m%d")} </TextField>
        <TextField id="S2AcessContG[0]">{S2AcessContG}</TextField>"""

#####################################################################################################


    signCapacity = "董事 Director"
    if appointee.capacity == "alternateDirector":
        signCapacity = "Alternate Director"

    if alreadyADirectorB == "yes":
        S2BexistAppointG = "S2BexistAppointG1[0]"
    elif alreadyADirectorB == 'no':
        S2BexistAppointG = "S2BexistAppointG2[0]"

    if appointee.companyOrPerson == "Natural Person":
        xml += f"""<TextField id="S2BCount">1</TextField>
<TextField id="S2Bcapacity1[0]">false</TextField>
<TextField id="S2Bcapacity2[0]">{appointeeCapacity[0]}</TextField>
<TextField id="S2Bcapacity3[0]">{appointeeCapacity[1]}</TextField>
<TextField id="S2BalternateTo[0]">{appointee.alternateTo}</TextField>
<TextField id="S2BchnName[0]">{appointee.directorNameInChinese}</TextField>
<TextField id="S2BengSurname[0]">{appointee.directorSurname}</TextField>
<TextField id="S2BengOthName[0]">{appointee.directorOtherName}</TextField>
<TextField id="S2BchnpreName[0]"/>
<TextField id="S2BengpreName[0]"/>
<TextField id="S2Bchnalias[0]"/>
<TextField id="S2Bengalias[0]"/>
<TextField id="S2Baddr1[0]">{appointee.address1}</TextField>
<TextField id="S2Baddr2[0]">{appointee.address2}</TextField>
<TextField id="S2Baddr3[0]">{appointee.address3}</TextField>
<TextField id="S2Bcountry[0]">Hong Kong</TextField>
<TextField id="S2BemailAddr[0]">{appointee.directorEmail}</TextField>
<TextField id="S2BHKID[0]">{appointee.hkidCardNumber[:-1]}({appointee.hkidCardNumber[-1]})</TextField>
<TextField id="S2BPPTNum[0]">{appointee.passportNumber}</TextField>
<TextField id="S2BissueCountry[0]">{appointee.passportIssuingCountry}</TextField>
<TextField id="S2BappointDate[0]">{cessation_date.strftime("%Y%m%d")}</TextField>
<TextField id="S2BexistAppointG[0]">{S2BexistAppointG}</TextField>

<TextField id="S2BSignName[0]">{appointee.directorSurname}, {appointee.directorOtherName}</TextField>
<TextField id="S2BSignCapacity[0]">{signCapacity}</TextField>
<TextField id="S2BnameCapacity[0]">{appointee.directorNameInChinese}##{appointee.directorSurname}, {appointee.directorOtherName}##D</TextField>
<TextField id="S2BnameCRNo[0]">{appointee.directorNameInChinese}##{appointee.directorSurname}, {appointee.directorOtherName}##</TextField>
<TextField id="S2BsignatoryCRNo[0]"/> 

<TextField id="S2CCount">0</TextField>

<TextField id="signName">{appointee.directorSurname}, {appointee.directorOtherName}</TextField>
<TextField id="signCapacity">{signCapacity}</TextField>
<TextField id="nameCapacity">{appointee.directorNameInChinese}##{appointee.directorSurname}, {appointee.directorOtherName}##D</TextField>
<TextField id="nameCRNo">{appointee.directorNameInChinese}##{appointee.directorSurname}, {appointee.directorOtherName}##</TextField>
<TextField id="signDate">{cessation_date.strftime("%Y%m%d")}</TextField>
<TextField id="signatoryCRNo"/>
</Eform>"""

    elif appointee.companyOrPerson == "Corporate":
        xml += f"""<TextField id="S2BCount">0</TextField>

<TextField id="S2CCount">1</TextField>
<TextField id="S2Ccapacity1[0]">false</TextField>
<TextField id="S2Ccapacity2[0]">{appointeeCapacity[0]}</TextField>
<TextField id="S2Ccapacity3[0]">{appointeeCapacity[1]}</TextField>
<TextField id="S2CalternateTo[0]">{appointee.alternateTo}</TextField>
<TextField id="S2CchnName[0]">{appointee.directorNameInChinese}</TextField>
<TextField id="S2CengName[0]">{appointee.directorOtherName}</TextField>
<TextField id="S2Caddr1[0]">{appointee.address1}</TextField>
<TextField id="S2Caddr2[0]">{appointee.address2}</TextField>
<TextField id="S2Caddr3[0]">{appointee.address3}</TextField>
<TextField id="S2Ccountry[0]">Hong Kong</TextField>
<TextField id="S2CemailAddr[0]">{appointee.directorEmail}</TextField>
<TextField id="S2CcompNo[0]">{appointee.companyNumber}</TextField>
<TextField id="S2CappointDate[0]">{cessation_date.strftime("%Y%m%d")}</TextField>
<TextField id="S2CexistAppointG[0]">{S2BexistAppointG}</TextField>

<TextField id="signName">{appointee.directorOtherName}</TextField>
<TextField id="signCapacity">{signCapacity}</TextField>
<TextField id="nameCapacity">{appointee.directorNameInChinese}##{appointee.directorOtherName}##D</TextField>
<TextField id="nameCRNo">{appointee.directorNameInChinese}##{appointee.directorOtherName}##{appointee.companyNumber}</TextField>
<TextField id="signatoryCRNo">{appointee.companyNumber}</TextField>
<TextField id="signDate">{cessation_date.strftime("%Y%m%d")}</TextField>
</Eform>
"""
    return xml

def send_board_resolution_notice(emailList, domain):
    pass