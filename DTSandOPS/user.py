__author__ = "stefanotuv"

from DTSandOPS import db, login

from werkzeug.security import generate_password_hash, check_password_hash
from DTSandOPS import bcrypt

from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    columns = ['user_id','user_name','email','password_hash']

    def columns(self):
        return self.columns

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.user_name)

    def set_password(self, password):
        # self.password_hash = generate_password_hash(password)
        self.password_hash = bcrypt.generate_password_hash(password).decode('UTF-8')

    def check_password(self, password):
        # return check_password_hash(self.password_hash, password)
        return bcrypt.check_password_hash(self.password_hash, password)
        # return check_password_hash(self.password_hash, bcrypt.generate_password_hash(password).decode('UTF-8'))