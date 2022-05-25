""""
recomment -
Author：wiki
Date：2022/5/20
"""
from models import *
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash


class Recomment():
    @staticmethod
    def add_recomment(UserId, ReUserId, CommentId, ReCommentDescribe):
        """
        增加回复的留言
        :param UserId:回复者的Id
        :param ReUserId:被回复者的Id
        :param CommentId:被回复留言的Id
        :param ReCommentDescribe:回复的内容
        :return:'回复者的Id不存在' or '被回复者的Id不存在' or '回复的留言Id不存在' or True
        """
        user = UserModel.query.filter_by(UserId=UserId).first()
        if user is None:
            return '回复者的Id不存在'
        user = UserModel.qusery.filter_by(UserId=ReUserId).first()
        if user is None:
            return '被回复者的Id不存在'
        comment = CommentModel.query.filter_by(CommentId=CommentId).first()
        if comment is None:
            return '回复的留言Id不存在'
        recomment = ReCommentModel(UserId=UserId, ReUserId=ReUserId, CommentId=CommentId,
                                   ReCommentDescribe=ReCommentDescribe)
        db.session.add(recomment)
        db.session.commit()
        return True

    @staticmethod
    def get_recomment(recommentid):
        recomment = ReCommentModel.query.filter_by(RecommentId=recommentid)
        if recomment is None:
            return '回复留言的Id不存在'
        recomment_json = dict()
        



