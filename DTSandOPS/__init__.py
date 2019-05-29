__author__ = "stefanotuv"

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# the secret key in python can be generate from the module secrets
#
# python
# >> import secrets
# >> secret.token_hex(16)
app.config['SECRET_KEY'] = 'stefanotuv'

# require the installation of pyMongo
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://stefano:stefano@localhost/DTSOPS'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(STATIC_DIR, 'db_local/role_tool_DB2.db')


# to allow to post/ save the user tables when querying for new role/tools
app.config['user_table'] = ''

db = SQLAlchemy(app)
login = LoginManager(app)
bcrypt = Bcrypt(app)

from DTSandOPS import views


