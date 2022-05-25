from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash,Response
import Function.function
from models import EmailCaptchaModel, UserModel
import string
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, logout_user, login_user, login_required, fresh_login_required
from forms import *
import os,uuid

bp=Blueprint('image',__name__,url_prefix="/image")

# 设置允许上传的文件格式
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']

# 设置图片返回的域名前缀
image_url_prefix = "/image/"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS


# 图片获取地址 用于存放静态文件
@bp.route("/<imageId>")
def get_frame(imageId):
    # 图片上传保存的路径
    try:
        with open(r'./static/images/{}'.format(imageId), 'rb') as f:
            image = f.read()
            result = Response(image, mimetype="image/jpg")
            return result
    except BaseException as e:
        return {"code": '503', "data": str(e), "message": "图片不存在"}


# 上传图片
@bp.route("/upload", methods=['POST', "GET"])
def uploads():
    if request.method == 'POST':
        cnt=0
        image_names=""
        for file in request.files.getlist('image'):
            # 检测文件格式
            if file and allowed_file(file.filename):
                # secure_filename方法会去掉文件名中的中文，获取文件的后缀名
                file_name_hz = secure_filename(file.filename).split('.')[-1]
                # 使用uuid生成唯一图片名
                first_name = str(uuid.uuid4())
                # 将 uuid和后缀拼接为 完整的文件名
                file_name = first_name + '.' + file_name_hz
                # 保存原图到cache，正式提交表单才将其放入到指定位置
                file.save(".\\static\\images\\"+file_name)
                cnt+=1
                image_names+=file_name+"\n"
        if cnt>0:
            return {"code": '200', "image_names": image_names, "message":"成功上传"+str(cnt)+"张图片","cnt":cnt}
        else:
            return {"code":'503',"message":"图片上传失败，仅支持png、jpg、jpeg类型"}
    return {"code": '503', "data": "", "message": "仅支持post方法"}