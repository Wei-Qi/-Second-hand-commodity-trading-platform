""""
ALIPAY -
Author：wiki
Date：2022/5/29
"""
from alipay import AliPay, DCAliPay, ISVAliPay
from alipay.utils import AliPayConfig
from models import *
from exts import db
from datetime import datetime

app_private_key_string = '-----BEGIN PRIVATE KEY-----\n' \
                         'MIIEogIBAAKCAQEArR/frQlSKDTbpgesYf61ISLxsGrMbToapQIRoPlFQzR6x7kk9ppneesav3Fq0EamD6lBdsKkoLBVDohtAmy4cf48BlPQk+1uBiu5JqQYHwzKJFzdmFySf6ULiFn5hSujteaeMDlN7YMRkpvZFuBIHlpqFZAFSk23+iCdhEZFAMBaRcoeFM+2OI2/PkfC9g3mu0K+2dmhsprnfgIGzsPjpkSbvdx6VXnR6WesLZCNCJYmlyXDLMok34kvoMWeWlrJkX0m8D72+in18W63gjPxea+BSXTseGf6+jF0s2wCHjzQyuNr5eowErQBw7P72loZPdbUB5934lmTEWBhsEyevQIDAQABAoIBADRpnu0jEkVr40e7sPumAi47BxLS8nrrCWAFZVLnxIlZHQbUTZV/H26wt9NXwe+2Q9Yf9tq+iNrBJ68TrHT8d0bDomaD/3SZgCLMH+zL5yWXWKdzmf7jn9KXJAuuubUQhiqu3BtbbfVHJg3NswaS9iKCWvWWOZPKPbWzJB0ErSVRl0LxZTan+IFdCJFvw+aMWEO4Vnp5hyrXln2s5TmfsONat9n24G5W5Wt8lsJ/vAvYrdzxrF0S5R4hdFJpeCAUu/Y+FHzjBnSYD7HoVJEEnqkrAG/hINIEK9Doa/Wv85GQuN+SFZxltugPzNFu4OyNGy6/PyqjZObqL9gPA5YuS/0CgYEA1wKkAXq5t0L8mBD/40s0Qk3BVspOBCNX4GXgJdQkdqmMcP2bP8pu6LiaVqhCw1N3gdDjOOA5p6Bd+4W8U9298lVXz2u6TtMxu42hVrdWruvcALi/ct6Xx1Bb5xvSAi7NPnWO6x0jx+T0nkL2l7t0mRiOlaSh3qMxdy4VYPUGxuMCgYEAziEJ9M9H5qjNeTSUTeCMKizN4KNBBHPv9OXzAUsSRyFkwxiGWwduoAcw8FMejrWdERv9mQl+VTWw3k4iGH6+Tzqsp5dp8bBczMhqjRhrVZnXw+EpfGYZkWmaI3D47wAdd4SbDVAbHxAMtyJmbFI4+IQB4xbsNj3DFbrsMwX0Vd8CgYBD17J2QQoumDVpqhuD1av0q+Iwh38ccSZ+SMb0SL8ErjUBRhRhiXd7eRxB8a+3QDP6QzYfMSkgCkr9XVJySApyV5lwenZ7/sm3e1YILattYEC3/ZNzJGdR3bpR7wZR6ACdD6z75OLwZP8GnOyALgb5c7Ux5JOq02V9TI40XLw5rwKBgF+FS/nYfHdVTjKWvQsBvbJlpNoujRilKVORo/S7dzLjNLB8EvboEMmzy2fy/LwhSTH+iJx8m8Cc6uN5za8QPNy2UgAv2HaZxcdYMJhF8qdubWBmXTU6kyqhhz5ZQeJvaThTiQ64SnkwlNPg6xnTWHdBpSY5HylboaXWQ1K5tap9AoGAVyuk2+rJ269EXZkhEpTcK7M9seEQ19U7Z0k5RxvisPe0oLRAbIwfvW5bTTvHJDwdjKuplezz1V+UDyDdvAQMkRZgowxUx6/39jLwHSVoxqUxsZKWZ8Sb1Metj2AXBVZpJeBqe9DEpbhtltUS6rJAeLBdkPufc6BiG/dvoflmO4A=\n' \
                         '-----END PRIVATE KEY-----'

alipay_public_key_string = '-----BEGIN PUBLIC KEY-----\n' \
                           'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4o0PSkUGBO/LwcpB0Xgf6LZAPCQ7Ly0KKknS8R9xFhjrcClm5Y2SjfkCkUKZk83P1bTWBkB+Bdz6rjzUp5V84vn36nUIRcdNYO+mhvrqg9yYbt04d73Ti0NNCFf/du5E/fO1ZU/p/FBBT7WUkqe2fjLjpXhPae8jCxv6BlUtRDTk+d0+tW6XRruTR1H4MZ/q2kR/pzR5NL00Mou7f1hv0h0Vd/ua7Rq6NOz0djABRD8RAp/NtNGTPb4M7239Jenw0cAeFR4d/ELIJHPsiUmSW8QRuWRKEyVw7J9EAMRseGcdfZjOMX9rxov7hQR8hxAHrfaqrUzJ7lLn+mONM9YS7wIDAQAB\n' \
                           '-----END PUBLIC KEY-----'

alipay = AliPay(
    appid="2021000120608347",
    app_notify_url=None,  # 默认回调 url
    app_private_key_string=app_private_key_string,
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2",  # RSA 或者 RSA2
    debug=True,  # 默认 False
    verbose=False,  # 输出调试数据
    config=AliPayConfig(timeout=15)  # 可选，请求超时时间
)


# 电脑网站支付，需要跳转到：https://openapi.alipaydev.com/gateway.do? + order_string
# 使用示例
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no="231231230",
    total_amount=10000,
    subject='被子',
    return_url="http://127.0.0.1:5000/",
    notify_url=None  # 可选，不填则使用默认 notify url
)
url = 'https://openapi.alipaydev.com/gateway.do?' + order_string

print(url)


class ALIPAY():
    @staticmethod
    def get_alipay_url(orderid, return_url):
        """
        根据订单返回
        :param orderid:
        :param return_url:
        :return: '订单id不存在' or url
        """
        order = OrderModel.query.filter_by(OrderId=orderid).first()
        if order is None:
            return '订单id不存在'
        amount = order.GoodsNum * order.goods.GoodsPrice
        url_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=str(orderid),
            total_amount=amount,
            subject=order.goods.GoodsName,
            return_url=return_url,
            notify_url=None  # 可选，不填则使用默认 notify url
        )
        url = 'https://openapi.alipaydev.com/gateway.do?' + url_string
        return url

    @staticmethod
    def check_valid(data):
        """
        检验返回的url，并修改订单的状态
        :param orderid:订单id
        :param data:返回的url中的数据， 为字典
        :return:'订单id不存在' or True or '校验失败'
        """
        orderid = int(data['out_trade_no'])
        order = OrderModel.query.filter_by(OrderId=orderid).first()
        if order is None:
            return '订单id不存在'
        signature = data.pop("sign")
        # verify
        success = alipay.verify(data, signature)
        if success:
            order.OrderState = 1
            order.AliId = int(data['trade_no'])
            db.session.commit()
            return True
        else:
            return '支付失败'

    @staticmethod
    def refund(orderid):
        """
        根据订单id进行退款
        :param orderid:订单id
        :return:'订单id不存在' or '该订单无法退款' or True or False
        """
        order = OrderModel.query.filter_by(OrderId=orderid).first()
        if order is None:
            return '订单id不存在'
        if order.OrderState == 0 or order.OrderState == 3 or order.OrderState == 4:
            return '该订单无法退款'
        amount = order.GoodsNum * order.goods.GoodsPrice
        result = alipay.api_alipay_trade_refund(
            refund_amount=amount,
            out_trade_no=str(orderid),
            trade_no=str(order.AliId)
        )
        # {'code': '10000', 'msg': 'Success', 'buyer_logon_id': 'sco***@sandbox.com', 'buyer_user_id': '2088622959321784',
        #  'fund_change': 'Y', 'gmt_refund_pay': '2022-05-30 18:25:05', 'out_trade_no': '231231230',
        #  'refund_fee': '10000.00', 'send_back_fee': '0.00', 'trade_no': '2022053022001421780502206166'}
        if result["code"] == "10000":
            # order.OrderState = 4
            # db.session.commmit()
            return True
        else:
            return False

    @staticmethod
    def transform_money(orderid):
        """
        根据订单id向商家转账
        :param orderid:订单id
        :return:
        """
        order = OrderModel.query.filter_by(OrderId=orderid).first()
        if order is None:
            return '订单id不存在'
        amount = order.GoodsNum * order.goods.GoodsPrice

        result = alipay.api_alipay_fund_trans_toaccount_transfer(
            datetime.now().strftime("%Y%m%d%H%M%S"),
            payee_type="ALIPAY_LOGONID",
            payee_account=str(order.seller.UserAliaccount),
            amount=amount
        )
        # result = {'code': '10000', 'msg': 'Success', 'order_id': '', 'out_biz_no': '',
        #           'pay_date': '2017-06-26 14:36:25'}
        if result["code"] == "10000":
            order.OrderState = 3
            db.session.commit()
            return True
        else:
            return False
