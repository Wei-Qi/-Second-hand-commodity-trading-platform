""""
user -
Author：wiki
Date：2022/5/8
"""

from models import UserModel, EmailCaptchaModel
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
import json


class user:
    @staticmethod
    def add_user(email, password, username):
        """
        注册时添加用户
        :param email:邮箱
        :param password:密码（原始）
        :param username:用户名
        :return:'该邮箱已被注册' or '该用户名已经被注册' or True
        """
        user = UserModel.query.filter_by(UserEmail=email).first()
        if user is not None:
            return '该邮箱已被注册'
        user = UserModel.query.filter_by(UserName=username).first()
        if user is not None:
            return '该用户名已经被注册'
        hash_password = generate_password_hash(password)
        user = UserModel(UserEmail=email, UserName=username, UserPassword=hash_password)
        db.session.add(user)
        db.session.commit()
        return True

    @staticmethod
    def change_password(email, password):
        """
        修改密码
        :param email: 邮箱
        :param password: 密码（原始）
        :return:'该邮箱不存在' or True
        """
        user = UserModel.query.filter_by(UserEmail=email).first()
        if user is None:
            return '该邮箱不存在'
        hash_password = generate_password_hash(password)
        user.UserPassword = hash_password
        db.session.commit()
        return True

    @staticmethod
    def email_isexist(email):
        """
        邮箱是否存在
        :param email:邮箱
        :return:True or False
        """
        user = UserModel.query.filter_by(UserEmail=email).first()
        if user is not None:
            return True
        else:
            return "该邮箱不存在"

    @staticmethod
    def username_isexist(username):
        """
        用户名是否存在
        :param username:用户名
        :return:True or ""
        """
        user = UserModel.query.filter_by(UserName=username).first()
        if user is not None:
            return True
        else:
            return "用户名不存在"

    @staticmethod
    def get_user(email):
        """
        通过邮箱获取用户
        :param email: 邮箱
        :return: 用户对象
        """
        user = UserModel.query.filter_by(UserEmail=email).first()
        return user

    @staticmethod
    def validate_user(email, password):
        """
        验证用户密码
        :param email: 邮箱
        :param password:密码
        :return: "该邮箱未注册" or "密码错误" or True
        """
        user = UserModel.query.filter_by(UserEmail=email).first()
        if user is None:
            return "该邮箱未注册"

        if check_password_hash(user.UserPassword, password):
            return True
        else:
            return "密码错误"

    @staticmethod
    def get_userinfo_by_email(email):
        """
        通过邮箱获取用户信息
        :param email: 邮箱
        :return: 用户信息（字典） or '邮箱不存在'
        """
        user = UserModel.query.filter_by(UserEmail=email).first()
        if user is None:
            return '邮箱不存在'
        user_json = dict(user)
        return user_json

    @staticmethod
    def get_userinfo_by_id(id):
        """
        通过id获取用户信息
        :param id: 用户id
        :return: 用户信息（json） or '用户id不存在'
        """
        user = UserModel.query.filter_by(UserId=id).first()
        if user is None:
            return '用户id不存在'
        user_json = dict(user)
        return user_json

#需要修改的地方
#1.如果函数正常执行，返回值用True就好，不要用字符串。错误信息用字符串。


#需要增添的方法：
#1.验证密码 validate_user(email,password) 验证email和password是否正确,正确返回True,错误返回信息(账户不存在、密码错误等)
#2.获取用户信息 按ID获取和按email获取  以json的形式返回所有信息
#3.根据邮箱，获取用户的验证码，获取完将验证码字段清空

