from flask import Flask
import config
from exts import db

from exts import mail
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
