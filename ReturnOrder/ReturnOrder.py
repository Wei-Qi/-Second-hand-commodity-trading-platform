""""
ReturnOrder -
Author：wiki
Date：2022/5/31
"""
from models import *
from exts import db
from payment.ALIPAY import ALIPAY

_Return_Order_State = {0: '待发货', 1: '待收货', 2: '确认收货'}


class ReturnOrder():
    """
    0：待发货
    1：待收货
    2：确认收货
    """

    @staticmethod
    def add_returnorder(orderid):
        """
        根据订单生成退货订单
        :param orderid:订单id
        :return:'订单id不存在' or '该订单无法生成退货订单' or True
        """
        order = OrderModel.query.filter_by(OrderId=orderid).first()
        if order is None:
            return '订单id不存在'
        if order.OrderState != 5:
            return '该订单无法生成退货订单'
        userid = order.UserId
        sellerid = order.SellerId
        return_order = ReturnOrderModel(SellerId=sellerid, UserId=userid, OrderId=orderid)
        db.session.add(return_order)
        db.session.commit()
        return True

    @staticmethod
    def get_returnorder_by_id(returnorderid):
        """
        根据退货订单id获取退货订单信息
        :param returnorderid:退货订单id
        :return:'退货订单id不存在' or True
        """
        return_order = ReturnOrderModel.query.filter_by(ReturnOrderId=returnorderid).first()
        if return_order is None:
            return '退货订单id不存在'
        return_order_dict = dict()
        return_order_dict['id'] = return_order.ReturnOrderId
        return_order_dict['买家id'] = return_order.UserId
        return_order_dict['买家姓名'] = return_order.user.UserName
        return_order_dict['买家头像'] = return_order.user.UserImage
        return_order_dict['id'] = return_order.ReturnOrderId
        return_order_dict['商品id'] = return_order.order.GoodsId
        return_order_dict['商品名称'] = return_order.order.goods.GoodsName
        return_order_dict['商品价格'] = return_order.order.goods.GoodsPrice
        return_order_dict['商品图片'] = return_order.order.goods.GoodsPicture.first().picturepath
        return_order_dict['商品库存'] = return_order.order.goods.GoodsStock
        return_order_dict['商品数量'] = return_order.order.GoodsNum
        return_order_dict['卖家id'] = return_order.SellerId
        return_order_dict['卖家姓名'] = return_order.seller.UserName
        return_order_dict['卖家头像'] = return_order.user.UserImage
        return_order_dict['卖家支付宝账户'] = return_order.user.UserAliaccount
        return_order_dict['时间'] = return_order.ReturnOrderTime
        return_order_dict['订单状态'] = _Return_Order_State[return_order.ReturnOrderState]
        return return_order_dict

    @staticmethod
    def get_returnorder_by_userid(userid):
        """
        根据用户获取退货订单的所有信息
        :param userid: 用户id
        :return: '用户id不存在' or return_order_json
        """
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户id不存在'
        return_order_json = []
        for return_order in user.UserReturnOrder:
            return_order_json.append(ReturnOrder.get_returnorder_by_id(return_order.ReturnOrderId))
        return return_order_json

    @staticmethod
    def get_retrunorder_by_sellerid(userid):
        """
        根据卖家id获取退货订单的所有信息
        :param userid:卖家id
        :return:'用户id不存在' or return_order_json
        """
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户id不存在'
        return_order_json = []
        for return_order in user.SellerReturnOrder:
            return_order_json.append(ReturnOrder.get_returnorder_by_id(return_order.ReturnOrderId))
        return return_order_json

    @staticmethod
    def change_return_order_state(returnorderid, state):
        """
        根据退货订单id修改订单的状态
        :param returnorderid:退货订单的id
        :param state:状态
        :return:'退货订单id不存在' or True
        """
        return_order = ReturnOrderModel.query.filter_by(ReturnOrderId=returnorderid).first()
        if return_order is None:
            return '退货订单id不存在'
        return_order.ReturnOrderState = state
        db.session.commit()
        return True


    @staticmethod
    def deliver_return_order(returnorderid, express):
        """
        退货订单发货
        :param returnorderid:退货订单id
        :param express:物流单号
        :return:'退货订单id不存在' or '该退货订单无法发货' or True
        """
        return_order = ReturnOrderModel.query.filter_by(ReturnOrderId=returnorderid).first()
        if return_order is None:
            return '退货订单id不存在'
        if return_order.ReturnOrderState != 0:
            return '该退货订单无法发货'
        ReturnOrder.change_return_order_state(returnorderid, 1)
        return_order.ReturnOrderExpress = express
        db.session.commit()
        return True

    @staticmethod
    def confirm_return_order(returnorderid):
        """
        退货订单的确认收货
        :param returnorderid:退货订单id
        :return:'退货订单id不存在' or '该退货订单无法确认收货' or True or False
        """
        return_order = ReturnOrderModel.query.filter_by(ReturnOrderId=returnorderid).first()
        if return_order is None:
            return '退货订单id不存在'
        if return_order.ReturnOrderState != 1:
            return '该退货订单无法确认收货'
        amount = return_order.order.GoodsNum * return_order.order.goods.GoodsPrice
        result = ALIPAY.refund(amount=amount, orderid=return_order.order.OrderId, AliId=return_order.order.AliId)
        if result:
            ReturnOrder.change_return_order_state(returnorderid, 2)
            return True
        else:
            return False


