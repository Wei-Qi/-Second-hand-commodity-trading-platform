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
        """
        获取回复留言的信息
        :param recommentid:
        :return:
        """
        recomment = ReCommentModel.query.filter_by(RecommentId=recommentid)
        if recomment is None:
            return '回复留言的Id不存在'
        recomment_json = dict()
        recomment_json['回复Id'] = recomment.UserId
        recomment_json['被回复者Id'] = recomment.ReUserId
        recomment_json['回复的留言Id'] = recomment.CommentId
        recomment_json['回复的内容'] = recomment.ReCommentDescribe
        recomment_json['回复的时间'] = recomment.ReCommentTime
        return recomment

    @staticmethod
    def get_recomment_by_commentid(commentid):
        """
        通过留言Id获取所有的回复留言的信息
        :param commentid:留言Id
        :return:'被回复留言的Id不存在' or recomment_json
        """
        comment = CommentModel.query.filter_by(CommentId=commentid)
        if comment is None:
            return '被回复留言的Id不存在'
        recomment_json = []
        for recomment in comment.rerecommments:
            tmp_dict = Recomment.get_recomment(recomment.RecommentId)
            recomment_json.append(tmp_dict)
        return recomment_json

    @staticmethod
    def del_recomment_by_recommentid(recommentid):
        """
        通过回复留言的ID删除回复留言
        :param recommentid:回复留言的Id
        :return:'回复的留言Id不存在' or True
        """
        recomment = ReCommentModel.query.filter_by(RecommentId=recommentid)
        if recomment is None:
            return '回复的留言Id不存在'
        recomment.ReCommentDescribe = '该留言已经被删除'
        recomment.IS_del = True
        db.session.commit()
        return True

    @staticmethod
    def recomment_is_del(recommentid):
        """
        判断段回复留言石佛偶已经被删除了
        :param recommentid:回复留言的id
        :return:'回复留言的Id不存在' or Is_del
        """
        recomment = ReCommentModel.query.filter_by(RecommentId=recommentid)
        if recomment is None:
            return '回复留言的Id不存在'
        return recomment.Is_del
