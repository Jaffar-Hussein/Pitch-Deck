from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config.from_object(Config)


db = SQLAlchemy(app)
mail=Mail(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'

login_manager.login_message_category = 'info'

from app.users.routes import users
from app.pitch.routes import posts
from app.main.routes import main

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(posts)


