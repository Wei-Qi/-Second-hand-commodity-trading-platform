""""
goods -
Author：wiki
Date：2022/5/19
"""

from models import *
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
import json


class goods():
    @staticmethod
    def add_goods(userid, goodsname, goodsprice, goodsstock, goodsdescribe):
        """
        添加商品
        :param userid:用户id
        :param goodsname:商品的名称
        :param goodsprice:商品的价格
        :param goodsstock:商品的库存
        :param goodsdescribe:商品的描述
        :return: True or '用户id不存在'
        """
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户id不不存在'
        goods = GoodsModel(GoodsName=goodsname, GoodsPrice=goodsprice, GoodsStock=goodsstock,
                           GoodsDescribe=goodsdescribe, UserId=userid)
        db.session.add(goods)
        db.session.commit()
        return True

    @staticmethod
    def get_goods_info(goodsid):
        """
        通过商品id获取商品的全部信息
        :param goodsid:商品id
        :return:goods_json or '商品id不存在'
        """
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        if goods is None:
            return '商品id不存在'
        goods_json = dict()
        goods_json['商品ID'] = goods.GoodsId
        goods_json['商品名称'] = goods.GoodsName
        goods_json['商品价格'] = goods.GoodsPrice
        goods_json['商品库存'] = goods.GoodsStock
        goods_json['商品描述'] = goods.GoodsDescribe
        goods_json['商品创建的时间'] = goods.GoodsTime
        goods_json['用户id'] = goods.UserId
        goods_json['商品图片'] = []
        goodspicture = goods.GoodsPicture.all()
        for picture in goodspicture:
            goods_json['商品图片'].append(picture)
        return goods_json

    @staticmethod
    def get_goods_info_byuser(userid):
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户Id不存在'
        goods = user.UserGoods.all()
        goods_list = []
        for good in goods:
            tmp_dict = {}
            tmp_dict['商品ID'] = good.GoodsId
            tmp_dict['商品名称'] = good.GoodsName
            tmp_dict['商品价格'] = good.GoodsPrice
            tmp_dict['商品库存'] = good.GoodsStock
            tmp_dict['商品描述'] = good.GoodsDescribe
            tmp_dict['商品创建的时间'] = good.GoodsTime
            tmp_dict['用户id'] = good.UserId
            tmp_dict['商品图片'] = []
            goods_list.append(tmp_dict)
        return goods_list

    @staticmethod
    def del_goods(userid, goodsid):
        """
        根据商品id删除商品
        :param userid:用户id
        :param goodsid:商品id
        :return:True or '商品id不存在' or '不是该用户的商品's
        """
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        if goods is None:
            return '商品id不存在'
        if goods.UserId != userid:
            return '不是该用户的商品'
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).delete()
        db.session.commit()
        return True

    @staticmethod
    def change_goods_info(userid, goodsid, goodsname, goodsprice, goodsstock, goodsdescribe):
        """
        修改商品的信息
        :param userid:用户id
        :param goodsid:商品id
        :param goodsname:商品名称
        :param goodsprice:商品价格
        :param goodsstock:商品库存
        :param goodsdescribe:商品描述
        :return: True or '商品id不存在' or '不是该用户的商品'
        """
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        if goods is None:
            return '商品id不存在'
        if goods.UserId != userid:
            return '不是该用户的商品'
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        goods.GoodsName = goodsname
        goods.GoodsPrice = goodsprice
        goods.GoodsStock = goodsstock
        goods.GoodsDescribe = goodsdescribe
        db.session.commit()
        return True
