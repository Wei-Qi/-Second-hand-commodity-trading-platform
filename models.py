""""
models -
Author：wiki
Date：2022/5/6
"""
from exts import db
from datetime import datetime
from flask_login import UserMixin, LoginManager


class AdminModel(db.Model):
    __tablename__ = 'admin'
    AdminId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AdminEmail = db.Column(db.String(100), nullable=False, unique=True)
    AdminName = db.Column(db.String(200), nullable=False, unique=True)
    # AdminNick = db.Column(db.String(200), nullable=False)
    AdminPassword = db.Column(db.String(200), nullable=False)
    AdminSex = db.Column(db.Boolean)
    AdminJoin_time = db.Column(db.DateTime, default=datetime.now)


class UserModel(db.Model, UserMixin):
    __tablename__ = 'user'
    UserId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserEmail = db.Column(db.String(100), nullable=False, unique=True)
    UserName = db.Column(db.String(200), nullable=False, unique=True)
    UserIdcard = db.Column(db.String(18), unique=True)
    UserImage = db.Column(db.String(128), unique=True)
    UserSex = db.Column(db.Boolean)
    UserPhone = db.Column(db.String(20))
    UserPassword = db.Column(db.String(200), nullable=False)
    UserCredit = db.Column(db.Integer, default=100)
    UserJoin_time = db.Column(db.DateTime, default=datetime.now)
    # 一对多关系通常放在一的那一方
    UserAddresses = db.relationship('UserAddressModel', backref='user', lazy='dynamic')
    UserGoods = db.relationship('GoodsModel', backref='user', lazy='dynamic')
    UserComments = db.relationship('CommentModel', backref='user', lazy='dynamic')

    def keys(self):
        return (
            'UserId', 'UserEmail', 'UserName', 'UserIdcard', 'UserSex', 'UserAddresses', 'UserPhone', 'UserPassword',
            'UserCredit', 'UserJoin_time')

    def __getitem__(self, item):
        return getattr(self, item)

    def get_id(self):  # flask-login要求的函数
        return self.UserId


class EvaluationModel(db.Model):
    __tablename__ = 'evaluation'
    EvaluationId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    EvaluationDescribe = db.Column(db.String(1024), nullable=False)
    EvaluationPicture = db.Column(db.BLOB)
    EvaluationScore = db.Column(db.Integer)
    EvaluationTime = db.Column(db.DateTime, default=datetime.now)
    UserId = db.Column(db.Integer), db.ForeignKey('user.UserId', ondelete='CASCADE')
    OrderId = db.Column(db.Integer, db.ForeignKey('order.OrderId', ondelete='CASCADE'))


class GoodsModel(db.Model):
    __tablename__ = 'goods'
    GoodsId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    GoodsName = db.Column(db.String(1024), nullable=False)
    GoodsPrice = db.Column(db.Float, nullable=False)
    GoodsStock = db.Column(db.Integer, nullable=False)
    GoodsDescribe = db.Column(db.String(1024), nullable=False)
    GoodsTime = db.Column(db.DateTime, default=datetime.now)
    UserId = db.Column(db.Integer, db.ForeignKey('user.UserId', ondelete='CASCADE'))
    Goods_Is_Takedown = db.Column(db.Boolean, default=False)
    # 一对多关系通常放在一的那一方
    GoodsPicture = db.relationship('GoodsPictureModel', backref='goods', lazy='dynamic')
    GoodsMessage = db.relationship('MessageRemindModel', backref='goods', lazy='dynamic')


class OrderModel(db.Model):
    __tablename__ = 'order'
    OrderId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderExpress = db.Column(db.String(200), unique=True)
    OrderNum = db.Column(db.Integer, nullable=False)
    OrderAddress = db.Column(db.String(200), nullable=False)
    OrderPhone = db.Column(db.String(11), nullable=False)
    OrderTime = db.Column(db.DateTime, default=datetime.now)
    OrderIsfinished = db.Column(db.Boolean)
    UserId = db.Column(db.Integer, db.ForeignKey('user.UserId', ondelete='CASCADE'))
    GoodsId = db.Column(db.Integer, db.ForeignKey('goods.GoodsId', ondelete='CASCADE'))


class CommentModel(db.Model):
    __tablename__ = 'comment'
    CommentId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CommentDescribe = db.Column(db.String(1024), nullable=False)
    CommentTime = db.Column(db.DateTime, default=datetime.now)
    UserId = db.Column(db.Integer, db.ForeignKey('user.UserId', ondelete='CASCADE'))
    GoodsId = db.Column(db.Integer, db.ForeignKey('goods.GoodsId', ondelete='CASCADE'))
    Is_del = db.Column(db.Boolean, default=False)

    goods = db.relationship('GoodsModel', backref=db.backref('comments', order_by=CommentTime.desc()))


class ReCommentModel(db.Model):
    __tablename__ = 'recomment'
    RecommentId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey('user.UserId', ondelete='CASCADE'))
    ReUserId = db.Column(db.Integer, db.ForeignKey('user.UserId', ondelete='CASCADE'))
    CommentId = db.Column(db.Integer, db.ForeignKey('comment.CommentId', ondelete='CASCADE'))
    ReCommentDescribe = db.Column(db.String(1024), nullable=False)
    ReCommentTime = db.Column(db.DateTime, default=datetime.now)
    Is_del = db.Column(db.Boolean, default=False)
    # 评论与回复评论的关系
    comments = db.relationship('CommentModel', backref=db.backref('recomments', order_by=ReCommentTime.desc()))
    # 用户 与 回复评论的关系
    user = db.relationship('UserModel', backref='recomments', foreign_keys=[UserId])
    # 用户 与 被回复评论的关系
    reuser = db.relationship('UserModel', backref='rerecommments', foreign_keys=[ReUserId])

class ReturnModel(db.Model):
    __tablename__ = 'return'
    ReturnId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ReturnAddress = db.Column(db.String(200), nullable=False)
    ReturnReason = db.Column(db.String(200), nullable=False)
    ReturnTime = db.Column(db.DateTime, default=datetime.now)
    ReturnExpress = db.Column(db.String(200), unique=True)
    ReturnIsfinished = db.Column(db.Boolean)
    UserId = db.Column(db.Integer, db.ForeignKey('user.UserId', ondelete='CASCADE'))
    OrderId = db.Column(db.Integer, db.ForeignKey('order.OrderId', ondelete='CASCADE'))

class EmailCaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

class UserAddressModel(db.Model):
    __tablename__ = 'useraddress'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(200), nullable=False)
    UserId = db.Column(db.Integer, db.ForeignKey('user.UserId', ondelete='CASCADE'))

class GoodsPictureModel(db.Model):
    __tabelname__ = 'goodspicture'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    picturepath = db.Column(db.String(1024), nullable=False)
    GoodsId = db.Column(db.Integer, db.ForeignKey('goods.GoodsId', ondelete='CASCADE'))

class MessageRemindModel(db.Model):
    __tablename__ = 'messageremind'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserId = db.Column(db.Integer, db.ForeignKey('user.UserId', ondelete='CASCADE'))
    MakerId = db.Column(db.Integer, db.ForeignKey('user.UserId', ondelete='CASCADE'))
    GoodsId = db.Column(db.Integer, db.ForeignKey('goods.GoodsId', ondelete='CASCADE'))
    Create_time = db.Column(db.DateTime, default=datetime.now)
    # 用户 与 留言提醒的关系
    user = db.relationship('UserModel', backref='messages', foreign_keys=[UserId])
    # 留言者 与 留言提醒的关系
    maker = db.relationship('UserModel', backref='makemessages', foreign_keys=[MakerId])
