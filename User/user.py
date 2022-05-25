""""
user -
Author：wiki
Date：2022/5/8
"""

from models import *
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
        if user_json['UserSex'] == 0:
            user_json['UserSex'] = '男'
        else:
            user_json['UserSex'] = '女'
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
        if user_json['UserSex'] == 0:
            user_json['UserSex'] = '男'
        else:
            user_json['UserSex'] = '女'
        return user_json

    @staticmethod
    def change_user_info(id, name, sex, phone):
        """
        通过id修改用户信息
        :param id: 用户id
        :param name:姓名
        :param sex:性别
        :param phone:手机号码
        :return: '该昵称已经被注册' or '用户id不存在' or True
        """
        user = UserModel.query.filter_by(UserName=name).first()
        if user is not None and user.UserId != id:
            return '该昵称已经被注册'
        user = UserModel.query.filter_by(UserId=id).first()
        if user is None:
            return '用户id不存在'
        user.UserName = name
        user.UserSex = sex
        user.UserPhone = phone
        db.session.commit()
        return True

    def get_user_address(id):
        """
        通过id获取用户的全地址信息
        :param id: 用户id
        :return: '改昵称已经被注册' or user_address_json
        """
        user = UserModel.query.filter_by(UserId=id).first()
        if user is None:
            return '用户id不存在'
        print(type(user.UserAddresses))
        useraddress = user.UserAddresses.all()
        user_address_json = []
        for address in useraddress:
            tmp_dict = {}
            tmp_dict['地址id'] = address.id
            tmp_dict['收货人'] = address.person_name
            tmp_dict['收货地址'] = address.address
            tmp_dict['电话号码'] = address.phone
            user_address_json.append(tmp_dict)
        return user_address_json

    @staticmethod
    def add_user_adddress(userid, person_name, address_name, phone):
        """
        增加用户的地址信息
        :param userid: 用户id
        :param person_name: 收件人姓名
        :param address_name: 地址
        :param phone: 电话
        :return: '用户id不存在' or True
        """
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户id不存在'
        address = UserAddressModel(person_name=person_name, address=address_name, phone=phone, UserId=userid)
        db.session.add(address)
        db.session.commit()
        return True

    @staticmethod
    def del_user_address(userid, addressid):
        """
        删除用户的地址信息
        :param userid: 用户id
        :param addressid: 地址id
        :return: '地址id不存在' or '不是该用户的地址' or True
        """
        address = UserAddressModel.query.filter_by(id=addressid).first()
        if address is None:
            return '地址id不存在'
        if address.UserId != userid:
            return '不是该用户的地址'
        address = UserAddressModel.query.filter_by(id=addressid).delete()
        db.session.commit()
        return True


    @staticmethod
    def change_user_address(userid, addressid, person_name, address_name, phone):
        """
        修改用户的地址信息
        :param userid: 用户id
        :param addressid: 地址id
        :param person_name: 收件人
        :param address_name: 地址
        :param phone: 电话
        :return: '地址id不存在' or '不是该用户的地址' or True
        """
        address = UserAddressModel.query.filter_by(id=addressid).first()
        if address is None:
            return '地址id不存在'
        if address.UserId != userid:
            return '不是该用户的地址'
        address.person_name = person_name
        address.address = address_name
        address.phone = phone
        db.session.commit()
        return True

    @staticmethod
    def change_user_image(userid, picturepath):
        """
        改变用户的头像
        :param userid:用户id
        :param picturepath:图片路径
        :return:'用户Id不存在' or True
        """
        user = UserModel.query.filter_by(UserId=userid)
        if user is None:
            return '用户Id不存在'
        user.UserImage = picturepath
        db.session.commit()
        return True

