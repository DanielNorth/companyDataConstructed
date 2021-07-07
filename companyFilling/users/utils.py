import os
from flask import url_for, current_app
from flask_mail import Message
from companyFilling import mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='daniel@hspector.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def send_confirmation_mail(user):
    token = user.get_reset_token()
    msg = Message("Email Confirmation",
                  sender='daniel@hspector.com',
                  recipients=[user.email])
    msg.body = f"""To confirm your account, please click the link below to verify you are the owner of this email
{url_for('users.confirm_email', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)


def send_email_to_myself(subject, message_body):
    msg = Message(subject,
                  sender='daniel@hspector.com',
                  recipients=['danielsplash10@gmail.com'])
    msg.body = message_body
    mail.send(msg)


def four_messages():
    from companyFilling.model import UserMessage
    from flask_login import current_user
    try:
        messages = UserMessage.query.filter_by(user_id=current_user.id).order_by(UserMessage.id.desc()).limit(4).all()
        return messages

    except:
        return None


def unread_messages_count():
    from companyFilling.model import UserMessage
    from flask_login import current_user
    try:
        messages = UserMessage.query.filter_by(user_id=current_user.id, read=False).count()
        return messages

    except:
        return 0