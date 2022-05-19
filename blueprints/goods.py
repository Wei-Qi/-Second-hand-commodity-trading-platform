from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
import Function.function
from models import EmailCaptchaModel, UserModel
import string
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, logout_user, login_user, login_required, fresh_login_required
from forms import *

bp=Blueprint('goods',__name__,url_prefix="/goods")

@bp.route('/upload',methods=['POST','GET'])
def upload():
    return render_template('subsimtgoods.html')