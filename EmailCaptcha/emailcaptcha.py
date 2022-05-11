""""
emialcaptcha -
Author：wiki
Date：2022/5/11
"""
from models import EmailCaptchaModel
from models import UserModel, EmailCaptchaModel
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
import json

class emailcaptcha():
    @staticmethod
    def get_captcha_by_email(email):
        """
        通过邮箱获取验证码，并将数据删除
        :param email: 邮箱
        :return: 验证码 or '请先获取验证码'
        """
        emailcaptcha = EmailCaptchaModel.query.filter_by(email=email).first()
        if emailcaptcha is None:
            return '请先获取验证码'
        captcha = emailcaptcha.captcha
        EmailCaptchaModel.query.filter_by(email=email).delete()
        db.session.commit()
        return captcha
