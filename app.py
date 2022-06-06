from flask import Flask, render_template, request
import config
from exts import db
from blueprints import user_bp, goods_bp, image_bp, cart_bp,order_bp,admin_bp

from exts import mail
from flask_migrate import Migrate
from models import *
from Function import function
from User.user import user
from Goods.goods import goods
from Comment.comment import Comment
from Comment.recomment import Recomment
from Comment.message import Message
from Cart.Cart import Cart
from Order.Order import Order
from payment.ALIPAY import ALIPAY
from Evaluation.Evaluation import Evaluation
from ReturnOrder.ReturnOrder import ReturnOrder
login_manager = LoginManager()

login_manager.login_view = '/user/login'  # 未登录将自动跳转到该路径
login_manager.login_message = '请先登陆'


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)
login_manager.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(goods_bp)
app.register_blueprint(image_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)
app.register_blueprint(admin_bp)

@app.route('/')
@app.route('/home')
def home():
    print(goods.get_goods_state_0())
    return render_template('index.html')

@app.errorhandler(404)  # 传入错误码作为参数状态
def errorDate(error):  # 接受错误作为参数
    return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(debug=True)
