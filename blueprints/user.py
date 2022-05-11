""""
user -
Author：wiki
Date：2022/5/6
"""

<<<<<<< Updated upstream
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
=======
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash

import Function.function
>>>>>>> Stashed changes
from exts import mail, db
from flask_mail import Message
# from models import EmailCaptchaModel, UserModel
import string
import random
from datetime import datetime
# from .forms import RegisterFrom
from werkzeug.security import generate_password_hash, check_password_hash
<<<<<<< Updated upstream

bp = Blueprint('user', __name__, url_prefix='/user')

=======
from flask_login import current_user, logout_user, login_user, login_required, fresh_login_required
from forms import *
from User.user import user

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
            return redirect(url_for('user.info'))
        else:
            flash(res)
    return render_template("login.html", form=form)


@bp.route('/forget_password', methods=['GET', 'POST'])
def forgetPassword():
    if current_user.is_authenticated:
        flash("请先退出登陆")
        return redirect(url_for('user.info'))
    return render_template('forget-password.html')


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@bp.route("/info")
@login_required
def info():
    return render_template("profile-details.html")


@bp.route('/signin', methods=['GET', 'POST'])
def signIn():
    if current_user.is_authenticated:
        return redirect(url_for('user.info'))
    form = RegistrationForm()
    if form.validate_on_submit():
        res = user.add_user(form.email, form.password, form.username)
        if res is True:
            return "sucess"
        else:
            flash(res)
    return render_template('signin.html', form=form)


@bp.route("/change_password")
@fresh_login_required  # 必须是新登入的
def change_password():
    return ''


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@bp.route('/captcha', methods=['POST'])
def get_captcha():
    # GET, POST
    email = request.form.get('email')
    if email:
        if Function.function.check_email_url(email) is False:
            return jsonify({'code': 400, 'message': '邮箱格式不正确'})
        Function.function.send_email(email)
        # 200 正常成功的请求
        return jsonify({'code': 200})
    else:
        # 400 客户端错误
        return jsonify({'code': 400, 'message': '请先输入邮箱'})
>>>>>>> Stashed changes
