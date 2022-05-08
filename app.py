from flask import Flask, render_template
import config
from exts import db
from blueprints import user_bp
from exts import mail
from flask_migrate import Migrate
from models import *
from Function import function

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)


@app.route('/')
def hello_world():  # put application's code here
    s = function.send_email('3339383816@qq.com')
    return s


if __name__ == '__main__':
    app.run()
