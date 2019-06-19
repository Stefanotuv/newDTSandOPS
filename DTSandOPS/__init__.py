__author__ = "stefanotuv"

from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from DTSandOPS.config import Config
from DTSandOPS.utilities.global_variable import *

db = SQLAlchemy()
bcrypt = Bcrypt()
login = LoginManager()
login.login_view = 'login'
login.login_message_category = 'info'


# from DTSandOPS import views

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['user_table'] = ''
    app.config['dbtype'] = ''
    app.config['connected'] = False
    app.config['SECRET_KEY'] = 'stefanotuv'
    app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER


    db.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)
    # from DTSandOPS import views
    from DTSandOPS.users.views import users
    from DTSandOPS.main.views import main
    from DTSandOPS.db_mng.views import db_mng
    from DTSandOPS.api.views import api_db

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(db_mng)
    app.register_blueprint(api_db)

    return app


