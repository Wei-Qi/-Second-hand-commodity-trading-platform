""""
Order -
Author：wiki
Date：2022/5/27
"""
from models import *
from exts import db
from payment.ALIPAY import ALIPAY

_Order_State = {0: '待支付', 1: '待发货', 2: '待收货', 3: '已完成', 4: '退货申请中', 5: '同意退货'}


class Order():
    """
    订单状态：
        0：待支付
        1：待发货
        2：待收货
        3：已完成
        4：退货申请中
        5：同意退货（修改了原来的名字）
    """

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
        addr = UserAddressModel.query.filter_by(id=addressid).first()
        if addr is None:
            return '地址id不存在'
        if goodsnum > goods.GoodsStock:
            return '商品库存不足'
        if goods.GoodsState != 1:
            return '商品没有上架，无法生成订单'
        if addr.UserId != user.UserId:
            return '该地址不属于该用户'
        order = OrderModel(UserId=userid, GoodsId=goodsid, GoodsNum=goodsnum,
                           SellerId=goods.user.UserId, OrderPersonName=addr.person_name, OrderPhone=addr.phone,
                           OrderAddress=addr.address)
        db.session.add(order)
        db.session.commit()
        goods.GoodsStock -= goodsnum
        db.session.commit()
        return int(order.OrderId)

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
    def deliver_goods(orderid, express):
        """
        发货
        :param orderid:订单id
        :param express:物流单号
        :return:'订单id不存在' or True
        """
        order = OrderModel.query.filter_by(OrderId=orderid).first()
        if order is None:
            return '订单id不存在'
        if order.OrderState != 1:
            return '该订单无法发货'
        expressorder = OrderModel.query.filter_by(OrderExpress=express).first()
        if expressorder is not None:
            return '物流单号重复'
        Order.change_order_state(orderid, 2)
        order.OrderExpress = express
        db.session.commit()
        return True

    @staticmethod
    def confirm_goods(orderid):
        """
        根据订单id确认收货
        :param orderid:
        :return:
        """
        order = OrderModel.query.filter_by(OrderId=orderid).first()
        if order is None:
            return '订单id不存在'
        if order.OrderState != 2:
            return '该订单无法确认收货'
        amount = order.GoodsNum * order.goods.GoodsPrice
        result = ALIPAY.transform_money(account=order.seller.UserAliaccount, amount=amount)
        if result:
            Order.change_order_state(orderid, 3)
            return True
        else:
            return '向卖家转账失败'

    @staticmethod
    def request_return(orderid, reason):
        """
        买家发起退货申请
        :param orderid:订单id
        :param reason:退货原因
        :return:'订单id不存在' or True
        """
        order = OrderModel.query.filter_by(OrderId=orderid).first()
        if order is None:
            return '订单id不存在'
        if order.OrderState == 0 or order.OrderState == 3 or order.OrderState == 4 or order.OrderState == 5:
            return '该订单无法申请退货'
        Order.change_order_state(orderid, 4)
        order.OrderReturnReason = reason
        db.session.commit()
        return True

    @staticmethod
    def check_request_return(orderid, is_agree):
        """
        卖家处理退货请求
        :param orderid:订单id
        :param is_agree:是否同意
        :return:'订单id不存在' or True
        """
        order = OrderModel.query.filter_by(OrderId=orderid).first()
        if order is None:
            return '订单id不存在'
        if order.OrderState != 4:
            return '该订单无法处理退货请求'
        if is_agree:
            Order.change_order_state(orderid, 5)
        else:
            Order.change_order_state(orderid, 2)
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
        order_dict['买家id'] = order.UserId
        order_dict['买家姓名'] = order.user.UserName
        order_dict['买家头像'] = order.user.UserImage
        order_dict['地址'] = order.OrderAddress
        order_dict['电话'] = order.OrderPhone
        order_dict['收件人'] = order.OrderPersonName
        order_dict['商品id'] = order.GoodsId
        order_dict['商品名称'] = order.goods.GoodsName
        order_dict['商品价格'] = order.goods.GoodsPrice
        order_dict['商品图片'] = order.goods.GoodsPicture.first().picturepath
        order_dict['商品库存'] = order.goods.GoodsStock
        order_dict['商品数量'] = order.GoodsNum
        order_dict['卖家id'] = order.SellerId
        order_dict['卖家姓名'] = order.seller.UserName
        order_dict['卖家头像'] = order.user.UserImage
        order_dict['卖家支付宝账户'] = order.user.UserAliaccount
        order_dict['时间'] = order.OrderTime
        order_dict['订单状态'] = _Order_State[order.OrderState]
        order_dict['支付宝账单'] = order.AliId
        order_dict['物流单号'] = order.OrderExpress
        order_dict['退货原因'] = order.OrderReturnReason
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
        for order in user.UserOrder:
            order_json.append(Order.get_order_by_orderid(order.OrderId))
        return order_json

    @staticmethod
    def get_order_by_sellerid(userid):
        """
        通过卖家id获取订单的所有信息
        :param userid:卖家id
        :return:
        """
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户id不存在'
        order_json = []
        for order in user.SellerOrder:
            order_json.append(Order.get_order_by_orderid(order.OrderId))
        return order_json

    @staticmethod
    def check_stock(goodsid, goodsnum):
        """
        检查库存是否足够
        :param goodsid:商品id
        :param goodsnum:需要购买的数量
        :return:'商品id不存在' or True or False
        """
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        if goods is None:
            return '商品id不存在'
        if goods.GoodsStock >= goodsnum:
            return True
        else:
            return False

    @staticmethod
    def get_request_return_order(userid):
        """
        根据用户id获取退货申请的订单
        :param userid:用户id
        :return:'用户id不存在' or order_json
        """
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户id不存在'
        order_json = []
        for order in user.SellerOrder:
            if order.OrderState == 4:
                order_json.append(Order.get_order_by_orderid(order.OrderId))
        return order_json
