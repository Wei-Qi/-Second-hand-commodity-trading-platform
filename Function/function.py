""""
function -
Author：wiki
Date：2022/5/8
"""
from exts import mail, db
from models import EmailCaptchaModel
import random
from flask_mail import Message
import string
from datetime import datetime


def send_email(email):
    """
    发送邮件
    :param email:邮箱
    :return:验证码
    """
    letters = string.ascii_letters + string.digits
    captcha = ''.join(random.sample(letters, 4))
    if email:
        message = Message(
            subject='【地摊货二手商品交易平台】',
            recipients=[email],
            body=f'【地摊货二手商品交易平台】您的邮箱验证码是：{captcha}，请不要告诉任何人哦'
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        return captcha


def check_email_url(email_address):
    # check '@'
    at_count = 0
    for element in email_address:
        if element == '@':
            at_count = at_count + 1

    if at_count != 1:
        return False

    # check ' '
    for element in email_address:
        if element == ' ':
            return False

    # check '.com'
    postfix = email_address[-4:]
    if postfix != '.com':
        return False

    # check char
    for element in email_address:
        if element.isalpha() == False and element.isdigit() == False:
            if element != '.' and element != '@' and element != '_':
                return False

    return True