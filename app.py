from flask import Flask, render_template
import config
from exts import db
from blueprints import user_bp
from exts import mail
from flask_migrate import Migrate
from models import *
from Function import function


login_manager = LoginManager()

login_manager.login_view = '/user/login'    #未登录将自动跳转到该路径
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


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
