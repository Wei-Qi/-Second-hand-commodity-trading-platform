""""
Order -
Author：wiki
Date：2022/5/27
"""
from models import *
from exts import db


class Order():
    @staticmethod
    def add_order(userid, addressid, goodsid, goodsnum):
        """
        增加订单
        :param userid:用户id
        :param addressid:订单id
        :param goodsid:商品id
        :param goodsnum:商品数量
        :return:'用户id不存在' Or '商品id不存在' or '商品库存不足' or '地址id不存在' or True
        """
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户id不存在'
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        if goods is None:
            return '商品id不存在'
        addr = UserAddressModel(id=addressid).first()
        if addr is None:
            return '地址id不存在'
        if goodsnum > goods.GoodsStock:
            return '商品库存不足'
        order = OrderModel(UserId=userid, GoodsId=goodsid, AddressId=addressid, GoodsNum=goodsnum)
        db.session.ad(order)
        db.session.commit()
        return True

    @staticmethod
    def change_order_state(orderid, state):
        """
        更改订单状态
        :param orderid:订单id
        :param state:订单状态
        :return:'订单id不存在' or True
        """
        order = OrderModel.query.filter_by(OrderId=orderid).first()
        if order is None:
            return '订单id不存在'
        order.OrderState = state
        db.session.commit()
        return True

    @staticmethod
    def get_order_by_orderid(orderid):
        """
        根据订单id获取订单信息
        :param orderid:订单id
        :return:'订单id不存在' or order_dict
        """
        order = OrderModel.query.filter_by(OrderId=orderid).first()
        if order is None:
            return '订单id不存在'
        order_dict = dict()
        order_dict['id'] = order.OrderId
        order_dict['用户id'] = order.UserId
        order_dict['地址id'] = order.AddressId
        order_dict['地址'] = order.address.address
        order_dict['电话'] = order.address.phone
        order_dict['收件人'] = order.address.person_name
        order_dict['商品id'] = order.GoodsId
        order_dict['商品名称'] = order.goods.GoodsName
        order_dict['商品价格'] = order.goods.GoodsPrice
        order_dict['商品图片'] = order.goods.GoodsPicture
        order_dict['商品数量'] = order.GoodsNum
        return order_dict

    @staticmethod
    def get_order_by_userid(userid):
        """
        通过用户id获取订单的所有信息
        :param userid:用户id
        :return:'用户id不存在' or order_json
        """
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户id不存在'
        order_json = []
        for order in user.UserOrder.all():
            order_json.append(Order.get_order_by_orderid(order.OrderId))
        return order_json