from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
import Function.function
from models import EmailCaptchaModel, UserModel
import string
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, logout_user, login_user, login_required, fresh_login_required
from forms import *
from Goods.goods import goods
from Comment.comment import Comment
from Comment.recomment import Recomment

bp=Blueprint('goods',__name__,url_prefix="/goods")

@bp.route('/upload',methods=['POST','GET'])
@login_required
def upload():
    form=UploadGoodsForm()
    if form.validate_on_submit():
        piclist=form.image_names.data.split()
        print(piclist)
        res=goods.add_goods(current_user.get_id(),form.goods_name.data,form.goods_price.data,form.goods_stock.data,form.goods_describe.data,piclist)
        if res is True:
            flash("上架成功")
            return redirect(url_for("user.myGoods"))
        else:
            flash(res)
    return render_template('subsimtgoods.html',form=form)

@bp.route('/<int:goodsid>')
def detail(goodsid):
    form=ReplyCommentForm()
    goodsInfo=goods.get_goods_info(goodsid)
    #print(goodsInfo['商品图片'])
    if goodsInfo == '商品id不存在':
        return '没有找到该商品的信息'
    comment_list=Comment.get_comment_by_goods(goodsid)
    recomment_dict={}
    for comment in comment_list:
        temp=Recomment.get_recomment_by_commentid(comment['评论Id'])
        recomment_dict[comment['评论Id']]=temp
    return render_template('product-single.html',form=form,goodsInfo=goodsInfo,comment_list=comment_list,recomment_dict=recomment_dict)

@bp.route('/add_comment/<int:goodsid>',methods=['POST'])
@login_required
def addComment(goodsid):
    comment=request.form.get('comment')
    if comment.strip() == '':
        flash('留言不能为空')
    else:
        res=Comment.add_comment(current_user.get_id(),goodsid,comment)
        if res is True:
            flash('留言成功')
        else:
            flash(res)
    return redirect('/goods/'+str(goodsid))

@bp.route('/reply_comment/<int:goodsid>',methods=['POST'])
def replyComment(goodsid):
    form=ReplyCommentForm()
    if form.validate_on_submit():
        res=Recomment.add_recomment(form.userid.data,current_user.get_id(),form.commentid.data,form.content.data)
        if res is True:
            flash('回复成功')
        else:
            flash(res)
    return redirect('/goods/'+str(goodsid))

@bp.route('/delete_comment/<int:goodsid>')
def deleteComment(goodsid):
    commentid=request.form.get('commentid')
    res=Comment.del_comment_by_commentId(commentid)
    if res is True:
        flash('删除成功')
    else:
        flash(res)
    return redirect('/goods/' + str(goodsid))

@bp.route('delete_recomment/<int:goodsid>')
def deleteRecomment(goodsid):
    recommentid = request.form.get('recommentid')
    res = Recomment.del_recomment_by_recommentid(recommentid)
    if res is True:
        flash('删除成功')
    else:
        flash(res)
    return redirect('/goods/' + str(goodsid))