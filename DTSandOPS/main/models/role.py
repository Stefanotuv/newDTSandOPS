__author__ = "stefanotuv"
from DTSandOPS import db

class Role(db.Model):
    __tablename__ = "roles"
    role_id = db.Column(db.Integer, primary_key=True)
    discipline = db.Column(db.String(25))
    core_role = db.Column(db.String(25))
    role = db.Column(db.String(25))
    columns = ['role_id','discipline','core_role','role']