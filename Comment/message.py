""""
message -
Author：wiki
Date：2022/5/27
"""
from models import *
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash


class Message():
    @staticmethod
    def add_message(userid, goodsid, makerid):
        """
        增加留言提醒信息
        :param userid:用户id（接受留言提醒者id）
        :param goodsid:商品id
        :param makerid:留言者id
        :return:'用户id不存在' or '留言者id不存在' or '商品id不存在' or True
        """
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户id不存在'
        maker = UserModel.query.filter_by(MakerId=makerid).first()
        if maker is None:
            return '留言者id不存在'
        goods = GoodsModel.query.filter_by(GoodsId=goodsid).first()
        if goods is None:
            return '商品id不存在'
        message = MessageRemindModel(UserId=userid, MakerId=makerid, GoodsId=goodsid)
        db.session.add(message)
        db.session.commit()
        return True

    @staticmethod
    def del_message_by_id(messageid):
        """
        根据留言提醒id删除留言提醒
        :param messageid:留言提醒id
        :return:'留言提醒id不存在' or True
        """
        message = MessageRemindModel.query.filter_by(id=messageid).first()
        if message is None:
            return '留言提醒id不存在'
        goods = MessageRemindModel.query.filter_by(id=messageid).delete()
        db.session.commit()
        return True

    @staticmethod
    def get_message_by_id(messageid):
        """
        根据留言提醒id获取留言提醒信息
        :param messageid:留言提醒id
        :return:'留言提醒id不存在' or message_dict
        """
        message = MessageRemindModel(id=messageid)
        if message is None:
            return '留言提醒id不存在'
        message_dict = dict()
        message_dict['留言提醒id'] = message.id
        message_dict['留言者id'] = message.MakerId
        message_dict['留言者姓名'] = message.maker.UserName
        message_dict['留言者头像'] = message.maker.UserImage
        message_dict['商品id'] = message.GoodsId
        message_dict['商品名称'] = message.goods.GoodsName
        return message_dict

    @staticmethod
    def get_meaasge_by_userid(userid):
        """
        根据用户id获取所有的留言提醒
        :param userid:用户id
        :return:'用户Id不存在' or message_json
        """
        user = UserModel.query.filter_by(UserId=userid).first()
        if user is None:
            return '用户Id不存在'
        messages = user.messages
        message_json = []
        for message in messages:
            message_json.append(Message.get_message_by_id(message.id))
        return message_json
