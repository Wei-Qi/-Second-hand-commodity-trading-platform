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
        添加评论
        :param UserId:用户id
        :param GoodsId:商品id
        :param CommentDescribe: 评论的描述
        :return: '商品id不存在' or '用户id不存在' or True
        """
        goods = GoodsModel.query.filter_by(GoodsId=GoodsId).first()
        if goods is None:
            return '商品id不存在'
        user = UserModel.query.filter_by(UserId=UserId).first()
        if user is None:
            return '用户id不存在'
        comment = CommentModel(UserId=UserId, GoodsId=GoodsId, CommentDescribe=CommentDescribe)
        db.session.add(comment)
        db.session.commit()
        return True

    @staticmethod
    def get_comment(CommentId):
        """
        根据评论Id获取评论的内容
        :param CommentId:评论的Id
        :return:'评论Id不存在' or comment_json
        """
        comment = CommentModel.query.filter_by(CommentId=CommentId).first()
        if comment is None:
            return '评论Id不存在'
        comment_json = dict()
        comment_json['评论Id'] = comment.CommentId
        comment_json['评论内容'] = comment.CommentDescribe
        comment_json['用户姓名'] = comment.user.UserName
        # comment_json['用户头像']
        comment_json['评论时间'] = comment.CommentTime

        return comment_json

    @staticmethod
    def get_comment_by_goods(GoodsId):
        """
        根据商品Id获取的所有的评论信息
        :param GoodsId:商品Id
        :return: '商品Id不存在' or comments_list（时间倒序）
        """
        goods = GoodsModel.querry.filter_by(GoodsId=GoodsId).first()
        if goods is None:
            return '商品Id不存在'
        comments = goods.comments.all()
        comments_list = []
        for comment in comments:
            tmp_dict = Comment.get_comment(comment.CommentId)
            comments_list.apppend(tmp_dict)
        return comments_list
