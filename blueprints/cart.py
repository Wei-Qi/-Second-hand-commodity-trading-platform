from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
import Function.function
from models import EmailCaptchaModel, UserModel
import string
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, logout_user, login_user, login_required, fresh_login_required
from forms import *
from Goods.goods import goods
from Cart.Cart import Cart

bp=Blueprint('cart',__name__,url_prefix="/cart")

@bp.route('/')
@login_required
def cart():

    cart_items=Cart.get_cart_by_userid(current_user.get_id())
    return render_template('cart.html',cart_items=cart_items)

@bp.route('/delete_item/<int:itemid>')
@login_required
def deleteItem(itemid):
    res=Cart.del_cart_by_id(itemid)
    if res is not True:
        flash(res)
    return redirect('/cart')

@bp.route('/add_item/<int:goodsid>',methods=['POST'])
@login_required
def addItem(goodsid):
    cnt=int(request.form.get('cnt',1))
    res=Cart.add_cart(current_user.get_id(),goodsid,cnt)
    if res is True:
        return jsonify({'code':200,'message':'添加成功,请到购物车中查看'})
    else:
        return jsonify({'code':400,'message':res})

@bp.route('/set_cnt/<int:itemid>',methods=['POST'])
@login_required
def setCnt(itemid):
    print(request.form)
    cnt=request.form.get('cnt')
    res=Cart.change_goods_num(itemid,cnt)
    if res is True:
        return jsonify({'code':200,'message':'修改成功'})
    else:
        return jsonify({'code':400,'message':res})

@bp.route('/checkout')
@login_required
def checkout():

    return render_template('checkout.html')
