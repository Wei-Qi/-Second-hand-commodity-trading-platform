""""
user -
Author：wiki
Date：2022/5/6
"""

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
import Function.function
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
import string
import random
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, logout_user, login_user, login_required, fresh_login_required
from forms import *
from User.user import user
from Goods.goods import goods
from Order.Order import Order
from ReturnOrder.ReturnOrder import ReturnOrder

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login', methods=['GET', 'POST'])
def logIn():
    if current_user.is_authenticated:
        return redirect(url_for('user.info'))
    form = LoginForm()
    if form.validate_on_submit():
        res = user.validate_user(form.email.data, form.password.data)
        if res is True:
            now_user = user.get_user(form.email.data)
            login_user(now_user, remember=True)  # 将用户记录在cookieID中，不用每次打开浏览器登陆一下
            return redirect(url_for('user.info', ispop=False))
        else:
            flash(res)
    return render_template("login.html", form=form)


@bp.route('/forget_password', methods=['GET', 'POST'])
def forgetPassword():
    form = ForgetPasswordForm()
    if current_user.is_authenticated:
        flash("请先退出登陆")
        return redirect(url_for('user.info', ispop=False))
    if form.validate_on_submit():
        res = user.change_password(form.email.data, form.password.data)
        if res is True:
            flash('密码修改成功,请登录')
            return redirect(url_for('user.logIn'))
        else:
            flash(res)
    return render_template('forget-password.html', form=form)

@bp.route('/signin', methods=['GET', 'POST'])
def signIn():
    if current_user.is_authenticated:
        flash('请先退出登陆')
        return redirect(url_for('user.info', ispop=False))
    form = RegistrationForm()
    if form.validate_on_submit():
        res = user.add_user(form.email.data, form.password.data, form.username.data,form.alipayaccount.data)
        if res is True:
            flash('账号创建成功，请登陆')
            return redirect(url_for('user.logIn'))
        else:
            flash(res)
    return render_template('signin.html', form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@bp.route("/info", methods=['post', 'get'])
@login_required
def info():
    form = ChangeUserInfoForm()
    if form.validate_on_submit():
        username = form.username.data
        usersex = form.usersex.data
        if usersex == '0':
            usersex = 0
        else:
            usersex = 1
        userphone = form.userphone.data
        res = user.change_user_info(current_user.get_id(), username, usersex, userphone)
        if res == '该昵称已经被注册':
            flash('该昵称被注册')
        user_info = user.get_userinfo_by_id(current_user.get_id())
        return render_template('profile-details.html', user_info=user_info, form=form, ispop=False)
    user_info = user.get_userinfo_by_id(current_user.get_id())
    return render_template("profile-details.html", user_info=user_info, form=form, ispop=False)



@bp.route("/address")
@login_required
def address():
    form1=AddAddressForm()
    form2=ChangeAddressForm()
    address_list=user.get_user_address(current_user.get_id())
    return render_template("address.html",form1=form1,form2=form2,address_list=address_list)


#两个函数用于处理address对应的页面中的两个表单
@bp.route('/address_add',methods=['POST'])
@login_required
def addAddress():
    form1 = AddAddressForm()
    form2 = ChangeAddressForm()
    if form1.is_submitted():
        if form1.validate():
            res=user.add_user_adddress(current_user.get_id(),form1.person_name.data,form1.address.data,form1.phone.data)
            if  res is True:
                flash("添加成功")
            else:
                flash("添加失败"+res)
                address_list = user.get_user_address(current_user.get_id())
                return render_template("address.html", form1=form1,form2=form2,address_list=address_list)
        else:
            flash("添加失败")
            address_list = user.get_user_address(current_user.get_id())
            return render_template("address.html", form1=form1, form2=form2, address_list=address_list)

    address_list=user.get_user_address(current_user.get_id())
    return render_template("address.html",form1=form1,form2=form2,address_list=address_list)


@bp.route('/address_change',methods=['POST'])
@login_required
def changeAddress():
    form1 = AddAddressForm()
    form2 = ChangeAddressForm()
    if form2.is_submitted():
        if form2.validate():
            res=user.change_user_address(current_user.get_id(),int(form2.address_id.data),form2.person_name.data,form2.address.data,form2.phone.data)
            if res is True:
                flash("修改成功")
            else:
                flash("修改失败"+res)
                address_list = user.get_user_address(current_user.get_id())
                return render_template("address.html", form1=form1,form2=form2,address_list=address_list)
        else:
            flash("修改失败")
            address_list = user.get_user_address(current_user.get_id())
            return render_template("address.html", form1=form1, form2=form2, address_list=address_list)
    address_list=user.get_user_address(current_user.get_id())
    return render_template("address.html",form1=form1,form2=form2,address_list=address_list)


@bp.route("/return_apply")
@login_required
def returnGoods():
    #applys=Order.#获取所有退货订单
    return render_template("return_apply.html")

@bp.route("/return_order")
@login_required
def returnOrder():
    order_list=ReturnOrder.get_retrunorder_by_sellerid(current_user.get_id())
    return render_template("return_order.html",order_list=order_list)

@bp.route("/my_purchase")
@login_required
def myPurchase():
    order_list=Order.get_order_by_userid(current_user.get_id())
    return render_template("mypurchase.html",order_list=order_list)

@bp.route("/my_sale",methods=['POST','GET'])
@login_required
def mySale():
    form=DelivergoodsForm()
    if form.validate_on_submit():#发货
        res=Order.deliver_goods(form.order_id.data,form.delivery_num.data)
        if res is True:
            flash("发货成功")
            sale_list = Order.get_order_by_sellerid(current_user.get_id())
            return render_template("mysale.html",sale_list=sale_list,form=form)
        else:
            flash(res)
            sale_list = Order.get_order_by_sellerid(current_user.get_id())
            return render_template("mysale.html",sale_list=sale_list,form=form)
    sale_list = Order.get_order_by_sellerid(current_user.get_id())
    return render_template("mysale.html",sale_list=sale_list,form=form)


@bp.route("/my_goods")
@login_required
def myGoods():
    goods_list=goods.get_goods_info_by_user(current_user.get_id())
    return render_template("myGoods.html",goods_list=goods_list)


@bp.route('/signin/captcha', methods=['POST'])
def signInCaptcha():
    email = request.form.get('email')
    res = user.get_userinfo_by_email(email)
    if res != '邮箱不存在':
        return jsonify({'code': 400, 'message': '邮箱已注册'})
    if email:
        if Function.function.check_email_url(email) is False:
            return jsonify({'code': 400, 'message': '邮箱格式不正确'})

        Function.function.send_email(email)
        # 200 正常成功的请求
        return jsonify({'code': 200})
    else:
        # 400 客户端错误
        return jsonify({'code': 400, 'message': '请先输入邮箱'})

@bp.route('/forget_password/captcha', methods=['POST'])
def forgetPasswordCaptcha():
    email = request.form.get('email')
    res=user.get_userinfo_by_email(email)
    if res=='邮箱不存在':
        return jsonify({'code': 400, 'message': '邮箱未注册'})
    if email:
        if Function.function.check_email_url(email) is False:
            return jsonify({'code': 400, 'message': '邮箱格式不正确'})

        Function.function.send_email(email)
        # 200 正常成功的请求
        return jsonify({'code': 200})
    else:
        # 400 客户端错误
        return jsonify({'code': 400, 'message': '请先输入邮箱'})


@bp.route('/address_delete',methods=['POST'])
@login_required
def deleteAddress():
    addressId=request.form.get('addressId')
    res=user.del_user_address(current_user.get_id(),addressId)
    if res is True:
        return jsonify({'code':200})
    else:
        return jsonify({'code':400,'message':res})