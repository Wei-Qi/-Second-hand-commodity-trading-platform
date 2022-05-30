""""
Evaluation -
Author：wiki
Date：2022/5/30
"""
from models import *
from exts import db

class Evaluation():
    @staticmethod
    def add_evaluation(userid, goodsid, describe, picture, score):
        """
        添加评论
        :param userid:用户id
        :param goodsid:商品id
        :param describe:商品描述
        :param picture:商品图片
        :param score:商品分数
        :return:'用户id不存在' or '商品id不存在' or True
        """
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户id不存在'
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        if goods is None:
            return '商品id不存在'
        evaluation = EvaluationModel(UserId=userid, GoodsId=goodsid, EvaluationDescribe=describe, EvaluationPicture=picture, EvaluationScore=score)
        db.session.add(evaluation)
        db.session.commit()
        return True

    @staticmethod
    def get_evaluation_by_evaluationid(evaluationid):
        """
        根据评价id获得评价的内容
        :param evaluationid: 评价id
        :return: '评价id不存在' or evaluation_dict
        """
        evaluation = EvaluationModel.query.filter_by(EvaluationId=evaluationid).first()
        if evaluation is None:
            return '评价id不存在'
        evaluation_dict = dict()
        evaluation_dict['id'] = evaluation.EvaluationId
        evaluation_dict['评价'] = evaluation.EvaluationDescribe
        evaluation_dict['图片'] = evaluation.EvaluationPicture
        evaluation_dict['分数'] = evaluation.EvaluationScore
        evaluation_dict['时间'] = evaluation.EvaluationTime
        evaluation_dict['用户id'] = evaluation.user.UserId
        evaluation_dict['用户姓名'] = evaluation.user.UserName
        evaluation_dict['用户头像'] = evaluation.user.UserImage
        return evaluation_dict

    @staticmethod
    def get_evaluation_by_goodsid(goodsid):
        """
        根据商品id获取评论
        :param goodsid:商品id
        :return:'商品id不存在' or evaluations_list
        """
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        if goods is None:
            return '商品id不存在'
        evaluations = goods.evaluations
        evaluations_list = []
        for evaluation in evaluations:
            tmp_dict = Evaluation.get_evaluation_by_evaluationid(evaluation.EvaluationId)
            evaluations_list.append(tmp_dict)
        return evaluations_list

