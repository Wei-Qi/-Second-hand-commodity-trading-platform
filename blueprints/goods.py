from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash,abort
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
from Evaluation.Evaluation import Evaluation

bp=Blueprint('goods',__name__,url_prefix="/goods")

@bp.route('/upload',methods=['POST','GET'])
@login_required
def upload():
    form=UploadGoodsForm()
    if form.validate_on_submit():
        piclist=form.image_names.data.split()
        #print(piclist)
        res=goods.add_goods(current_user.get_id(),form.goods_name.data,form.goods_price.data,form.goods_stock.data,form.goods_describe.data,piclist)
        if res is True:
            flash("已发出上架申请，请等待管理员审核")
            return redirect(url_for("user.myGoods"))
        else:
            flash(res)
    return render_template('subsimtgoods.html',form=form)

@bp.route('/reupload/<int:goodsid>')
@login_required
def reupload(goodsid):
    res=goods.take_up_goods(goodsid)
    if res is True:
        flash("已发起上架申请")
    else:
        flash(res)
    return redirect("/user/my_goods")

@bp.route('/change/<int:goodsid>',methods=['POST','GET'])
@login_required
def change(goodsid):
    goods1=goods.get_goods_info(goodsid)
    if goods1 == '商品id不存在':
        abort(404)
    form=UpdateGoodsForm(goods_name=goods1['商品名称'],goods_describe=goods1['商品描述'],goods_stock=goods1['商品库存'],goods_price=goods1['商品价格'])
    if form.validate_on_submit():
        piclist = form.image_names.data.split()
        res=goods.change_goods_info(current_user.get_id(),goodsid,form.goods_name.data,form.goods_price.data,form.goods_stock.data,form.goods_describe.data,piclist)
        if res is True:
            flash('修改成功')
            return redirect(f'/goods/{goodsid}')
        else:
            flash(res)
    return render_template('changegoods.html',form=form,goodsid=goodsid)

@bp.route('/<int:goodsid>')
def detail(goodsid):
    form=ReplyCommentForm()
    goodsInfo=goods.get_goods_info(goodsid)
    #print(goodsInfo['商品图片'])
    if goodsInfo == '商品id不存在':
        abort(404)
    comment_list=Comment.get_comment_by_goods(goodsid)
    recomment_dict={}
    for comment in comment_list:
        temp=Recomment.get_recomment_by_commentid(comment['留言Id'])
        recomment_dict[comment['留言Id']]=temp
    remark_list=Evaluation.get_evaluation_by_goodsid(goodsid)
    return render_template('product-single.html',form=form,goodsInfo=goodsInfo,comment_list=comment_list,recomment_dict=recomment_dict,remark_list=remark_list)

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
@login_required
def replyComment(goodsid):
    form=ReplyCommentForm()
    #print(form.userid.data,form.commentid.data,form.content.data)
    if form.validate_on_submit():
        #print('yes')
        res=Recomment.add_recomment(current_user.get_id(),form.userid.data,form.commentid.data,form.content.data)
        if res is True:
            flash('回复成功')
        else:
            flash(res)
    return redirect('/goods/'+str(goodsid))

@bp.route('/delete_comment/<int:goodsid>',methods=['POST'])
@login_required
def deleteComment(goodsid):
    commentid=request.form.get('commentid')
    if Comment.get_comment(commentid)['用户Id'] !=current_user.get_id():
        return jsonify({'code': 400, 'message': '无法删除别人的留言'})
    res=Comment.del_comment_by_commentId(commentid)
    if res is True:
        flash('删除成功')
        return jsonify({'code': 200, 'url': '/goods/' + str(goodsid) })
    else:
        return jsonify({'code': 400, 'message': res})

@bp.route('/delete_recomment/<int:goodsid>',methods=['POST'])
@login_required
def deleteRecomment(goodsid):
    recommentid = request.form.get('recommentid')
    if Recomment.get_recomment(recommentid)['回复者Id'] !=current_user.get_id():
        return jsonify({'code': 400, 'message': '无法删除别人的留言'})
    res = Recomment.del_recomment_by_recommentid(recommentid)
    if res is True:
        flash('删除成功')
        return jsonify({'code': 200, 'url': '/goods/' + str(goodsid) })
    else:
        return jsonify({'code': 400, 'message': res})

@bp.route('/withdraw/<int:goodsid>')
@login_required
def withdraw(goodsid):
    if goods.get_goods_info(goodsid)['用户id'] != current_user.get_id():
        flash('无法下架别人的商品')
    else:
        res=goods.take_down_goods(goodsid)
        if res is True:
            flash('下架成功')
        else:
            flash(res)
    return redirect('/user/my_goods')

@bp.route('/search')
def search():
    '''
    搜索结果页面
    '''
    query=request.args.get('query') #获取搜索关键字
    if query == '':
        abort(404)
    if query.lower() == 'all':
        query=''
    goods_list=goods.search_goods(query)
    return render_template('searchResults.html',goods_list=goods_list,query=query)
