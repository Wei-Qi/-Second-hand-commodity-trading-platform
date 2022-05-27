""""
Cart -
Author：wiki
Date：2022/5/27
"""
from models import *
from exts import db


class Cart():
    @staticmethod
    def add_cart(userid, goodsid, goodsnum):
        """
        添加购物车
        :param userid:用户id
        :param goodsid:商品id
        :param goodsnum:商品数量
        :return:'用户id不存在' or '商品id不存在' or True
        """
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户id不存在'
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        if goods is None:
            return '商品id不存在'
        cart = CartModel(UserId=userid, GoodsId=goodsid, GoodsNum=goodsnum)
        db.session.add(cart)
        db.session.commit()
        return True

    @staticmethod
    def get_cart_by_id(cartid):
        """
        根据id获取购物车的信息，已下架的商品不返回
        :param cartid:购物车id
        :return:'购物车id不存在' or None or cart_dict
        """
        cart = CartModel.query.filter_by(id=cartid).first()
        if cart is None:
            return '购物车id不存在'
        if cart.goods.Goods_Is_Takedown == True:
            return None
        cart_dict = dict()
        cart_dict['id'] = cart.id
        cart_dict['用户id'] = cart.UserId
        cart_dict['商品id'] = cart.GoodsId
        cart_dict['商品名称'] = cart.goods.GoodsName
        cart_dict['商品单价'] = cart.goods.GoodsPrice
        cart_dict['商品库存'] = cart.goods.GoodsStock
        cart_dict['商品数量'] = cart.GoodsNum
        return cart_dict

    @staticmethod
    def get_cart_by_usrid(userid):
        """
        根据用户返回购物车
        :param userid:用户id
        :return:'用户id不存在' or cart_json
        """
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户id不存在'
        carts =  user.UserCarts.all()
        cart_json = []
        for cart in carts:
            cart_json.append(Cart.get_cart_by_id(cart.id))
        return cart_json

    @staticmethod
    def change_goods_num(cartid, num):
        """
        修改购物车的数量
        :param cartid:购物车id
        :param num:修改后的数量
        :return:'购物车id不存在' or True
        """
        cart = CartModel.query.filter_by(id=cartid).first()
        if cart is None:
            return '购物车id不存在'
        cart.GoodsNum = num
        db.session.commit()
        return True

    @staticmethod
    def del_cart_by_id(cartid):
        """
        根据购物车id删除购物车
        :param cartid:购物车id
        :return:'购物车id不存在' or True
        """
        cart = CartModel.query.filter_by(id=cartid).first()
        if cart is None:
            return '购物车id不存在'
        cart = CartModel.query.filter_by(id=cartid).delete()
        db.session.commit()
        return True