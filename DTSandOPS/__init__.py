__author__ = "stefanotuv"

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from DTSandOPS.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login = LoginManager()
login.login_view = 'login'
login.login_message_category = 'info'

# from DTSandOPS import views

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)
    # from DTSandOPS import views
    from DTSandOPS.users.views import users

    app.register_blueprint(users)

    return app


