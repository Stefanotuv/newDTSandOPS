__author__ = "stefanotuv"
from DTSandOPS import db

class Tool(db.Model):
    __tablename__ = "tools"
    tool_id = db.Column(db.Integer, primary_key=True)
    tool_name = db.Column(db.String(25))
    tool_vendor = db.Column(db.String(25)) # SaaS/Desktop
    columns = ['tool_id','tool_name','tool_vendor']