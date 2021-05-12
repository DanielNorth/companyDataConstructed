import os
from flask import url_for, current_app
from flask_mail import Message
from companyFilling import mail


def send_d4_xml_email(companyName, fileLoc):
    msg = Message(f'resignation of director from company {companyName}',
                  sender='danielsplash10@gmail.com',
                  recipients=['asz24687@gmail.com'])
    msg.body = f'''Send this file to cr.
'''
    with open(fileLoc) as file:
        msg.attach(file)


    mail.send(msg)

