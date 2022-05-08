""""
user -
Author：wiki
Date：2022/5/8
"""

from models import UserModel
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash


class user:
    @staticmethod
    def add_user(email, password, username):
        """
        注册时添加用户
        :param email:邮箱
        :param password:密码（原始）
        :param username:用户名
        :return:'该邮箱已被注册' or '该用户名已经被注册' or '成功'
        """
        user = UserModel.query.filter_by(UserEmail=email)
        if user is not None:
            return '该邮箱已被注册'
        user = UserModel.query.filter_by(UserName=username)
        if user is not None:
            return '该用户名已经被注册'
        hash_password = generate_password_hash(password)
        user = UserModel(UserEmail=email, UserName=username, UserPassword=hash_password)
        db.session.add(user)
        db.session.commit()
        return '成功'

    @staticmethod
    def change_password(email, password):
        """
        修改密码
        :param email: 邮箱
        :param password: 密码（原始）
        :return:'该邮箱不存在' or '成功'
        """
        user = UserModel.query.filter_by(UserEmail=email)
        if user is None:
            return '该邮箱不存在'
        hash_password = generate_password_hash(password)
        user.UserPassword = hash_password
        db.session.commit()
        return '成功'

    @staticmethod
    def email_isexist(email):
        """
        邮箱是否存在
        :param email:邮箱
        :return:'该邮箱已存在' or '该邮箱不存在'
        """
        user = UserModel.query.filter_by(UserEmail=email)
        if user is not None:
            return '该邮箱已存在'
        else:
            return '该邮箱不存在'

    @staticmethod
    def username_isexist(username):
        """
        用户名是否存在
        :param username:用户名
        :return:'该用户名已经存在' or '该用户名不存在'
        """
        user = UserModel.query.filter_by(UserName=username)
        if user is not None:
            return '该用户名已经存在'
        else:
            return '该用户名不存在'
