from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash,abort
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
from Evaluation.Evaluation import Evaluation
from config import LocalAddress

bp=Blueprint('order',__name__,url_prefix="/order")

@bp.route('/create/<int:cartid>',methods=['POST'])
@login_required
def create(cartid):
    '''
    生成order并返回生成结果
    '''
    addressid=request.form.get('addressid')
    cartitem=Cart.get_cart_by_id(cartid)
    if cartitem == '购物车id不存在':
        return jsonify({'code':400,'message':'购物车id不存在'})
    res=Order.add_order(current_user.get_id(),addressid,cartitem['商品id'],cartitem['商品数量'])
    if type(res) == int:
        Cart.del_cart_by_id(cartid)
        return jsonify({'code':200,'url':'/order/'+str(res)})
    else:
        return jsonify({'code':400,'message':res})

@bp.route('/<int:orderid>')
@login_required
def order(orderid):
    order=Order.get_order_by_orderid(orderid)
    userid=current_user.get_id()
    if order == '订单id不存在':
        abort(404)
    return render_template('order_single.html',order=order,userid=userid)

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
    order = Order.get_order_by_orderid(orderid)
    if order == '订单id不存在':
        abort(404)
    alipay_url=ALIPAY.get_alipay_url(orderid,LocalAddress+'/order/pay/check/'+str(orderid))
    return redirect(alipay_url)

@bp.route('/evaluate/<int:orderid>',methods=['POST','GET'])
@login_required
def evaluate(orderid):
    order=Order.get_order_by_orderid(orderid)
    if order=='订单id不存在':
        abort(404)
    if order['买家id'] !=current_user.get_id():
        abort(404)
    if request.method=='POST':
        score=request.form.get('score','')
        content=request.form.get('content','')
        img=request.form.get('img','')
        if score.strip() == '' or content.strip()=='' or img.strip() == '':
            return jsonify({'code':400,'message':'请填写所有字段'})
        res=Evaluation.add_evaluation(current_user.get_id(),order['商品id'],content,img,score)
        if res is True:
            res=Order.confirm_goods(orderid)
            if res is True:
                flash('评价完成，订单已关闭')
            else:
                flash('评价完成，订单关闭异常:'+res)
            return jsonify({'code':200,'url':f"/goods/{order['商品id']}"})
        else:
            return jsonify({'code':400,'message':res})
    return render_template('evaluate.html')

@bp.route('/deny/<int:orderid>')
@login_required
def deny(orderid):
    res = Order.check_request_return(orderid, False)
    if res is True:
        flash('已拒绝退货申请')
    else:
        flash(res)
    return redirect(url_for("user.returnApply"))

@bp.route('/agree/<int:orderid>')
@login_required
def agree(orderid):
    res= Order.check_request_return(orderid,True)
    if res is True:
        flash('已同意，等待买家送货')
    else:
        flash(res)
    return redirect(url_for("user.returnApply"))
