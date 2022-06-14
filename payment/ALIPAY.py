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
                         'MIIEowIBAAKCAQEAmg00fEe41sILTzpQsugjcAbDGaamhspQhF5y9E7wb8IprzGETIPvrFmqK1lFcyO7kQiqnnz6MYQIOuwmC3DUSZ8qlaQAXnTNy+/hi4fC81MwXQ155S4GMTTXGGS0d9MoaJEPHAOZoSp0KYxcK1B/g4XZM14XQt4L49FZ2f9X1++7cS0GetbLa6E5LezxUGivQnGmY0rMJlW0lsfgsSZEL0FIRO9WbDaRtyjfr82cYnSpFrT+x/553l4qt9YoV4eR3FLm6tQri/ORFxqnH+0F9oJch2HV2pwJCVKwVvQYjl/wRRE9zWkzDmyCOTlFjwug5c7XHZFcm6kGqwT4s/vCmwIDAQABAoIBAHv/xQ+Ea7Px3UiYl/xp/pxd1Q0Ap2o3zze9Dqq4H7DViNgL84HjcTg5tE/QO6bCTGghobSQxJK2xCkpjDYJS9c21wA8Uk+1lTFilRnK3ZEelP9RqZxfv3w8HCb2aI1K2mvQ12ilPTQNCBOpd0cmNH2Zb4t5YR/hu5BVIw3mCr80YXA+DeAp6eoyy76Biomz5nXuP+9WiskAw5U3XJuxYo665l4GxNfnVhFDqAa+UVzUgeRlUgr3C52vovFWpk2g8aFmxTs7iOteWM/+bS1jBTlNYN1kJijLvYpI2TFfBIAgBLlXXxJg1fYTeBKwRTWW7/xcQvGqZqq1xaVTLNCc/oECgYEA9msUR+U6SN6cDB+gDMdyfHUEEfD3upIm+JjKYPHs2lKpDw390KH6Wq3qqGdTFkHyeCqfcZuYQVbEMhRv6kCSebwD9v5nLroqFLzW/F0JKxIy0p+O7aM8HhR8VzzjV/OnrhYEQ8s9aepWpJJM4noHvTgzsM7OAMfNuJ8uYDXjWV0CgYEAoAquJSn0qtRQxlLMMFdGj8ZqwZIgyEhr28xSM8tE6eZj8VkzCs37FF01jVeqoBWcDbSINDB4b47YeTdE5SnyEdNR7ueHwWLzURyT95LnViJqRv/ykc+NY0dsCIhwTnfpill27Euf+1g3zmdKYOEqh7qXWS0T1mgF7lUEFgc/tFcCgYEA5nrNI1niJBoitqw11P4PtRz1y5oo+1aMIOU4FWjyclnySmR5zFRUh9A3tX+/FQhls8OaEnbH+AUhyP2Yl/ABkN8sji7xb6Esjuz54F1cn+6LnrkixF5zcmcSzb3jnnYFlix9nLNSI+jNVWyJgSNGbdNNdchYoh4/6rjodZCxrvkCgYBHKPiNpb4YRxczV5Va2TOSshK9xw+0fh8XOB5E0Vju93Xw1kyPvU6qm1c4ZYaEb5dXsLHvIq4qTEWMgDqt+pybuG5x35jJMAooQqC4MCWUcvD2aM+ebb7cKeGrWZ82BLNexLDQGEAmLe+CYwL7WKLkft7U0+pCJzab5klO0iJNOQKBgBjt5NL9tCslcGOWjekzbHnKiSfPrc1/0asE3UmYD+F88+SMHNmOiW7O0l+SpBhxiPAsDp+55hoUNtqumiIrw73x3v+kA6vIDxysqQ2vm26+ZkFq05FyKbAlCsnLl8TY9kdkxjcT5fbM/TXvG6QBUGzC8Y5LW51gY43/2oZsSNiD\n' \
                         '-----END PRIVATE KEY-----'

alipay_public_key_string = '-----BEGIN PUBLIC KEY-----\n' \
                           'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsdqedaf3BFQbKfaMZvEmEUwxvBm6RVCIwfkd0iNxkLZrVc4kNp1NIQRAA/IZwhY75c0jGAEraLZfa9Iklt1ezl2C6JeYWiw4fffJTgqJSA7CE6kXw5ywrHyLPlr0eI7u6XbZ21020wI6BBFz8vFMTuuK2WjT6ESJwUTWb8YwgzaPNUT6x6/Q2JS1MMIwT/LrCuXGvH9zSjZT5vT+N+HCWhIj1svgNQgkEzxvVYO8xLuhO7iMyojAL0EahKvxW8mmZsuJdgmx3cCktw8tb+7vgnf3TLYiuzS+yK8n4RPgny8SjjDlOJn5v3aVd+1tQegH24ItiNNENphIbyrKO4ez7QIDAQAB\n' \
                           '-----END PUBLIC KEY-----'

alipay = AliPay(
    appid="2021000120609144",
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
# order_string = alipay.api_alipay_trade_page_pay(
#     out_trade_no="231231230",
#     total_amount=10000,
#     subject='被子',
#     return_url="http://127.0.0.1:5000/",
#     notify_url=None  # 可选，不填则使用默认 notify url
# )
# url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
# print(url)


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
        if order.OrderState != 0:
            return '该订单无法支付'
        amount = order.GoodsNum * order.goods.GoodsPrice
        amount = round(amount, 2)
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
            order.AliId = str(data['trade_no'])
            db.session.commit()
            return True
        else:
            return '支付失败'

    @staticmethod
    def refund(amount, orderid, AliId):
        """
        退款
        :param amount:退款金额
        :param orderid:订单id
        :param AliId:阿里的订单id
        :return:True or False
        """
        amount = round(amount, 2)
        result = alipay.api_alipay_trade_refund(
            refund_amount=amount,
            out_trade_no=str(orderid),
            trade_no=str(AliId)
        )
        # {'code': '10000', 'msg': 'Success', 'buyer_logon_id': 'sco***@sandbox.com', 'buyer_user_id': '2088622959321784',
        #  'fund_change': 'Y', 'gmt_refund_pay': '2022-05-30 18:25:05', 'out_trade_no': '231231230',
        #  'refund_fee': '10000.00', 'send_back_fee': '0.00', 'trade_no': '2022053022001421780502206166'}
        if result["code"] == "10000":
            return True
        else:
            return False

    @staticmethod
    def transform_money(amount, account):
        """
        向卖家转钱
        :param amount:金额
        :param account:卖家账户
        :return:
        """
        amount = round(amount, 2)
        result = alipay.api_alipay_fund_trans_toaccount_transfer(
            datetime.now().strftime("%Y%m%d%H%M%S"),
            payee_type="ALIPAY_LOGONID",
            payee_account=str(account),
            amount=amount
        )
        # result = {'code': '10000', 'msg': 'Success', 'order_id': '', 'out_biz_no': '',
        #           'pay_date': '2017-06-26 14:36:25'}
        if result["code"] == "10000":
            return True
        else:
            return False
