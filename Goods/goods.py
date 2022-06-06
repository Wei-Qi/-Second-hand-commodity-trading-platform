""""
goods -
Author：wiki
Date：2022/5/19
"""

from models import *
from exts import db
from sqlalchemy import or_

from werkzeug.security import generate_password_hash, check_password_hash
import json

_Order_State = {0: '上架申请中', 1: '上架中', 2: '已下架'}

class goods():
    @staticmethod
    def add_goods(userid, goodsname, goodsprice, goodsstock, goodsdescribe, goodspicturelist):
        """
        添加商品
        :param userid:用户id
        :param goodsname:商品的名称
        :param goodsprice:商品的价格
        :param goodsstock:商品的库存
        :param goodsdescribe:商品的描述
        :param:商品图片路径的一个列表
        :return: True or '用户id不存在'
        """
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户id不不存在'
        goods1 = GoodsModel(GoodsName=goodsname, GoodsPrice=goodsprice, GoodsStock=goodsstock,
                            GoodsDescribe=goodsdescribe, UserId=userid)
        db.session.add(goods1)
        db.session.commit()
        for picture in goodspicturelist:
            goods.add_goods_picture(goods1.GoodsId, picture)
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
            goods_json['商品图片'].append(picture.picturepath)
        goods_json['商品状态'] = _Order_State[goods.GoodsState]
        return goods_json

    @staticmethod
    def get_goods_info_by_user(userid):
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户Id不存在'
        goods1 = user.UserGoods.all()  # 不要再goods类里面将变量命名为goods，老是报错！！！
        goods_list = []
        for good in goods1:
            tmp_dict = goods.get_goods_info(good.GoodsId)
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
        if goods.Goods_Is_Takedown:
            return '该商品已经下架'
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        goods.GoodsName = goodsname
        goods.GoodsPrice = goodsprice
        goods.GoodsStock = goodsstock
        goods.GoodsDescribe = goodsdescribe
        db.session.commit()
        return True

    # @staticmethod
    # def get_goods_info_byuser(userid):
    #     user = UserModel.query.filter_by(UserId=userid).first()
    #     if user is None:
    #         return '用户Id不存在'
    #     goods = user.UserGoods.all()
    #     goods_list = []
    #     for good in goods:
    #         tmp_dict = {}
    #         tmp_dict['商品ID'] = good.GoodsId
    #         tmp_dict['商品名称'] = good.GoodsName
    #         tmp_dict['商品价格'] = good.GoodsPrice
    #         tmp_dict['商品库存'] = good.GoodsStock
    #         tmp_dict['商品描述'] = good.GoodsDescribe
    #         tmp_dict['商品创建的时间'] = good.GoodsTime
    #         tmp_dict['用户id'] = good.UserId
    #         tmp_dict['商品图片'] = []
    #         goods_list.append(tmp_dict)
    #     return goods_list

    @staticmethod
    def add_goods_picture(goodsid, picturepath):
        """
        增加商品图片
        :param goodsid:商品ID
        :param picturepath:路径
        :return:'商品的Id不存在' or True
        """
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        if goods is None:
            return '商品的Id不存在'
        goods_picture = GoodsPictureModel(GoodsId=goodsid, picturepath=picturepath)
        db.session.add(goods_picture)
        db.session.commit()
        return True

    @staticmethod
    def take_down_goods(goodsid):
        """
        根据商品id下架商品
        :param goodsid:商品id
        :return:'商品id不存在' or '商品已经下架' or True
        """
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        if goods is None:
            return '商品id不存在'
        if goods.GoodsState != 1:
            return '该商品无法下架'
        goods.GoodsState = 2
        db.session.commit()
        return True

    @staticmethod
    def search_goods(content):
        """
        搜索商品（只返回已经上架的商品）
        :param content:搜索的内容
        :return:goods_list
        """
        goods1 = GoodsModel.query.filter(
            or_(GoodsModel.GoodsName.like('%' + content + '%'), GoodsModel.GoodsDescribe.contains('%' + content + '%'))).order_by(
            db.text('-GoodsTime'))
        goods_list = []
        for item in goods1:
            if item.GoodsState == 1:
                goods_list.append(goods.get_goods_info(item.GoodsId))
        return goods_list

    @staticmethod
    def take_up_goods(goodsid):
        """
        根据商品id发出上架申请
        :param goodsid:商品id
        :return:'商品id不存在' or '该商品无法发起上架申请' or True
        """
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        if goods is None:
            return '商品id不存在'
        if goods.GoodsState != 2:
            return '该商品无法发起上架申请'
        goods.GoodsState = 0
        db.session.commit()
        return True

    @staticmethod
    def agree_shelf_request(goodsid):
        """
        将商品改为上架状态
        :param goodsid:
        :return:'商品id不存在' or  '该商品无法同意上架申请' or  True
        """
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        if goods is None:
            return '商品id不存在'
        if goods.GoodsState != 0:
            return '该商品无法同意上架申请'
        goods.GoodsState = 1
        db.session.commit()
        return True

    @staticmethod
    def refuse_shelf_request(goodsid):
        """
        拒绝上架申请
        :param goodsid:商品id
        :return:'商品id不存在' or '该商品无法拒绝上架申请' or True
        """
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        if goods is None:
            return '商品id不存在'
        if goods.GoodsState != 0:
            return '该商品无法拒绝上架申请'
        goods.GoodsState = 2
        db.session.commit()
        return True


    @staticmethod
    def get_goods_state_0():
        """
        获得所有的在上架申请中的商品
        :return:goods_json
        """
        goods_list = GoodsModel.query.filter_by(GoodsState=0).all()
        goods_json = []
        for goods1 in goods_list:
            goods_json.append(goods.get_goods_info(goods1.GoodsId))
        return goods_json

    @staticmethod
    def get_goods_state_1():
        """
        获得所有的已经上架的商品
        :return:goods_json
        """
        goods_list = GoodsModel.query.filter_by(GoodsState=1).all()
        goods_json = []
        for goods1 in goods_list:
            goods_json.append(goods.get_goods_info(goods1.GoodsId))
        return goods_json

    @staticmethod
    def get_goods_state_2():
        """
        获的所有已经下架的商品
        :return:goods_json
        """
        goods_list = GoodsModel.query.filter_by(GoodsState=2).all()
        goods_json = []
        for goods1 in goods_list:
            goods_json.append(goods.get_goods_info(goods1.GoodsId))
        return goods_json
