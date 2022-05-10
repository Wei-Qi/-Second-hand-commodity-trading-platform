""""
user -
Author：wiki
Date：2022/5/6
"""

from flask import Blueprint, render_template, request, redirect, url_for, jsonify,flash
from exts import mail, db
from flask_mail import Message
from models import EmailCaptchaModel, UserModel
import string
import random
from datetime import datetime
# from .forms import RegisterFrom
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user,logout_user,login_user,login_required
from forms import *
from User.user import user

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/login',methods=['GET','POST'])
def logIn():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        res=user.validate_user(form.email.data,form.password.data)
        if res is True:
            now_user=user.get_user(form.email.data)
            login_user(now_user)
            return redirect(url_for('info'))
        else:
            flash(res)
    return render_template("login.html", form=form)

@bp.route('/forget_password',methods=['GET','POST'])
def forgetPassword():
    return render_template('')

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@bp.route("/info")
@login_required
def info():
    return render_template("profile-details.html")