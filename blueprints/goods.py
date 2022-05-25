from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
import Function.function
from models import EmailCaptchaModel, UserModel
import string
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, logout_user, login_user, login_required, fresh_login_required
from forms import *
from Goods.goods import goods

bp=Blueprint('goods',__name__,url_prefix="/goods")

@bp.route('/upload',methods=['POST','GET'])
@login_required
def upload():
    form=UploadGoodsForm()
    if form.validate_on_submit():
        piclist=form.image_names.data.split('\n')
        res=goods.add_goods(current_user.get_id(),form.goods_name.data,form.goods_price.data,form.goods_stock.data,form.goods_describe.data,piclist)
        if res is True:
            flash("上架成功")
            return redirect(url_for("user.myGoods"))
        else:
            flash(res)
    return render_template('subsimtgoods.html',form=form)

@bp.route('/<int:goodsid>')
def detail(goodsid):
    goodsInfo=goods.get_goods_info(goodsid)
    if goodsInfo == '商品id不存在':
        return '没有找到该商品的信息'
    return render_template('product-single.html',goodsInfo=goodsInfo)
