from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash,abort
import Function.function
from models import EmailCaptchaModel, UserModel
import string
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, logout_user, login_user, login_required, fresh_login_required
from forms import *
from Goods.goods import goods as Goods
from User.user import user

bp=Blueprint('admin',__name__,url_prefix="/admin")

@bp.route('/')
@bp.route('/goods_manage')
@login_required
def goodsManage():
    nuser=user.get_userinfo_by_id(current_user.get_id())
    if nuser["UserIsAdmin"] is False:
        flash('需要管理员权限')
        abort(404)
    query = request.args.get('query', '')
    if query != '':
        goods_list = Goods.search_goods_state1(query)
    else:
        goods_list = Goods.get_goods_state_1()
    return render_template("goodsAdmin.html",goods_list=goods_list,nuser=nuser,query=query)

@bp.route('/goods_apply')
@login_required
def goodsApply():
    nuser = user.get_userinfo_by_id(current_user.get_id())
    if nuser["UserIsAdmin"] is False:
        flash('需要管理员权限')
        abort(404)
    query=request.args.get('query','')
    if query != '':
        goods_list=Goods.search_goods_state0(query)
    else:
        goods_list = Goods.get_goods_state_0()
    return render_template("goodsShelfApplication.html", goods_list=goods_list,nuser=nuser,query=query)

@bp.route('/goods_apply/agree/<int:goodsid>')
@login_required
def applyAgree(goodsid):
    nuser = user.get_userinfo_by_id(current_user.get_id())
    goods_list = Goods.get_goods_state_0()
    if nuser["UserIsAdmin"] is False:
        flash('需要管理员权限')
        abort(404)
    res=Goods.agree_shelf_request(goodsid)
    if res is True:
        flash('已同意')
    else:
        flash(res)
    query = request.args.get('query', '')
    return redirect(f'/admin/goods_apply?query={query}')

@bp.route('/goods_apply/deny/<int:goodsid>')
@login_required
def applyDeny(goodsid):
    nuser = user.get_userinfo_by_id(current_user.get_id())
    if nuser["UserIsAdmin"] is False:
        flash('需要管理员权限')
        abort(404)
    goods_list = Goods.get_goods_state_0()
    res=Goods.refuse_shelf_request(goodsid)
    if res is True:
        flash('已拒绝')
    else:
        flash(res)
    query = request.args.get('query', '')
    return redirect(f'/admin/goods_apply?query={query}')

@bp.route('/take_down_goods/<int:goodsid>')
@login_required
def takeDownGoods(goodsid):
    nuser = user.get_userinfo_by_id(current_user.get_id())
    if nuser["UserIsAdmin"] is False:
        flash('需要管理员权限')
        abort(404)
    res=Goods.take_down_goods(goodsid)
    if res is True:
        flash('已将商品下架')
    else:
        flash(res)
    query = request.args.get('query', '')
    return redirect(f'/admin/goods_manage?query={query}')