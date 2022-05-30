from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
import Function.function
from models import EmailCaptchaModel, UserModel
import string
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, logout_user, login_user, login_required, fresh_login_required
from forms import *
from Goods.goods import goods
from User.user import user
from Cart.Cart import Cart
from Order.Order import Order
from payment.ALIPAY import ALIPAY

bp=Blueprint('order',__name__,url_prefix="/order")

@bp.route('/create/<int:cartid>',methods=['POST'])
@login_required
def create(cartid):
    '''
    生成order并返回生成结果
    '''
    addressid=request.form.get('addressid')
    cartitem=Cart.get_cart_by_id(cartid)
    res=Order.add_order(current_user.get_id(),addressid,cartitem[''],cartitem[''])
    if type(res) == int:
        return jsonify({'code':200,'url':'/order/'+str(res)})
    else:
        return jsonify({'code':200,'message':res})

@bp.route('/<int:orderid>')
@login_required
def order(orderid):
    order=Order.get_order_by_orderid(orderid)
    return ''

@bp.route('/pay/check/<int:orderid>')
@login_required
def check(orderid):
    res=ALIPAY.check_valid(request.args.to_dict())
    if res is True:
        flash('支付成功')
        return redirect(f'/order/{orderid}')
    else:
        flash(res)
        return redirect(f'/order/{orderid}')

@bp.route('/pay/<int:orderid>')
@login_required
def pay(orderid):
    alipay_url=ALIPAY.get_alipay_url(orderid,'/order/pay/check/'+str(orderid))
    return redirect(alipay_url)