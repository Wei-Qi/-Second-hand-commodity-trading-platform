""""
comment -
Author：wiki
Date：2022/5/20
"""
from models import *
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash


class Comment():
    @staticmethod
    def add_comment(UserId, GoodsId, CommentDescribe):
        """
        添加留言
        :param UserId:用户id
        :param GoodsId:商品id
        :param CommentDescribe: 留言的描述
        :return: '商品id不存在' or '用户id不存在' or True
        """
        goods = GoodsModel.query.filter_by(GoodsId=GoodsId).first()
        if goods is None:
            return '商品id不存在'
        user = UserModel.query.filter_by(UserId=UserId).first()
        if user is None:
            return '用户id不存在'
        if goods.Goods_Is_Takedown:
            return '该商品已经下架'
        comment = CommentModel(UserId=UserId, GoodsId=GoodsId, CommentDescribe=CommentDescribe)
        db.session.add(comment)
        db.session.commit()
        meaasge = MessageRemindModel(MakerId=UserId, GoodsId=GoodsId, UserId=goods.UserId)
        db.session.add(meaasge)
        db.session.commit()
        return True

    @staticmethod
    def get_comment(CommentId):
        """
        根据留言Id获取留言的内容
        :param CommentId:留言的Id
        :return:'留言Id不存在' or comment_json
        """
        comment = CommentModel.query.filter_by(CommentId=CommentId).first()
        if comment is None:
            return '留言Id不存在'
        comment_json = dict()
        comment_json['留言Id'] = comment.CommentId
        comment_json['留言内容'] = comment.CommentDescribe
        comment_json['用户Id'] = comment.user.UserId
        comment_json['用户姓名'] = comment.user.UserName
        comment_json['用户头像'] = comment.user.UserImage
        comment_json['留言时间'] = comment.CommentTime
        comment_json['是否被删除'] = comment.Is_del
        return comment_json


    @staticmethod
    def get_comment_by_goods(GoodsId):
        """
        根据商品Id获取的所有的留言信息
        :param GoodsId:商品Id
        :return: '商品Id不存在' or comments_list（时间倒序）
        """
        goods = GoodsModel.query.filter_by(GoodsId=GoodsId).first()
        if goods is None:
            return '商品Id不存在'
        print(goods.comments)
        comments = goods.comments
        comments_list = []
        for comment in comments:
            tmp_dict = Comment.get_comment(comment.CommentId)
            comments_list.append(tmp_dict)
        return comments_list

    @staticmethod
    def del_comment_by_commentId(commentid):
        """
        根据留言Id删除留言
        :param commentid: 留言Id
        :return: '留言的Id不存在' or True
        """
        comment = CommentModel.query.filter_by(CommentId=commentid).first()
        if comment is None:
            return '留言的Id不存在'
        comment.CommentDescribe = '该留言已经被删除'
        comment.Is_del = True
        db.session.commit()
        return True

    @staticmethod
    def comment_is_del(commentid):
        """
        判断留言是否已经被删除
        :param commentid:留言Id
        :return:'留言的Id不存在' or Is_del
        """
        comment = CommentModel.query.filter_by(CommentId=commentid).first()
        if comment is None:
            return '留言的Id不存在'
        return comment.Is_del
