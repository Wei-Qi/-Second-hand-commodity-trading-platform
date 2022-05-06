""""
user -
Author：wiki
Date：2022/5/6
"""

from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from exts import mail, db
from flask_mail import Message
# from models import EmailCaptchaModel, UserModel
import string
import random
from datetime import datetime
# from .forms import RegisterFrom
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('user', __name__, url_prefix='/user')


# @bp.route('/login')
# def login():
#     return render_template('login.html')