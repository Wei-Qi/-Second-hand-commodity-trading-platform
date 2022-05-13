""""
user -
Author：wiki
Date：2022/5/6
"""


from flask import Blueprint, render_template, request, redirect, url_for, jsonify,flash
import Function.function
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
import string
import random
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('user', __name__, url_prefix='/user')


from flask_login import current_user, logout_user, login_user, login_required, fresh_login_required

from forms import *
from User.user import user

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/login',methods=['GET','POST'])
def logIn():
    if current_user.is_authenticated:
        return redirect(url_for('user.info'))
    form = LoginForm()
    if form.validate_on_submit():
        res = user.validate_user(form.email.data, form.password.data)
        if res is True:
            now_user = user.get_user(form.email.data)
            login_user(now_user, remember=True)  # 将用户记录在cookieID中，不用每次打开浏览器登陆一下
            return redirect(url_for('user.info'))
        else:
            flash(res)
    return render_template("login.html", form=form)


@bp.route('/forget_password', methods=['GET', 'POST'])
def forgetPassword():
    form = ForgetPasswordForm()
    if current_user.is_authenticated:
        flash("请先退出登陆")
        return redirect(url_for('user.info'))
    if form.validate_on_submit():
        res=user.change_password(form.email.data,form.password.data)
        if res is True:
            flash('密码修改成功,请登录')
            return redirect(url_for('user.logIn'))
        else:
            flash(res)
    return render_template('forget-password.html',form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@bp.route("/info")
@login_required
def info():
    user_info=user.get_userinfo_by_id(current_user.get_id())
    return render_template("profile-details.html", user_info=user_info)




@bp.route('/signin',methods=['GET','POST'])
def signIn():
    if current_user.is_authenticated:
        flash('请先退出登陆')
        return redirect(url_for('user.info'))
    form=RegistrationForm()
    if form.validate_on_submit():
        res = user.add_user(form.email.data, form.password.data, form.username.data)
        if res is True:
            flash('账号创建成功，请登陆')
            return redirect(url_for('user.logIn'))
        else:
            flash(res)
    return render_template('signin.html', form=form)


@bp.route("/change_password")
@fresh_login_required   #必须是新登入的
def change_password():
    return ''


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@bp.route("/order")
@login_required
def order():
    return render_template("order.html")

@bp.route("/address")
@login_required
def address():
    return render_template("address.html")

@bp.route("/return_goods")
@login_required
def returnGoods():
    return render_template("return_goods.html")

@bp.route("/return_order")
@login_required
def returnOrder():
    return render_template("return_order.html")

@bp.route("/order")
@login_required
def order():
    return render_template("order.html")


@bp.route("/address")
@login_required
def address():
    return render_template("address.html")


@bp.route("/return_goods")
@login_required
def returnGoods():
    return render_template("return_goods.html")


@bp.route("/return_order")
@login_required
def returnOrder():
    return render_template("return_order.html")


@bp.route('/captcha', methods=['POST'])
def getCaptcha():
    # GET, POST
    email = request.form.get('email')
    if email:
        if Function.function.check_email_url(email) is False:
            return jsonify({'code':400,'message':'邮箱格式不正确'})

        Function.function.send_email(email)
        # 200 正常成功的请求
        return jsonify({'code': 200})
    else:
        # 400 客户端错误
        return jsonify({'code': 400, 'message': '请先输入邮箱'})
