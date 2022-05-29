""""
ALIPAY -
Author：wiki
Date：2022/5/29
"""
from alipay import AliPay, DCAliPay, ISVAliPay
from alipay.utils import AliPayConfig

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
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no="30024020",
    total_amount=0.01,
    subject='被子',
    return_url="http://127.0.0.1:5000/",
    notify_url=None  # 可选，不填则使用默认 notify url
)
url = 'https://openapi.alipaydev.com/gateway.do?' + order_string


