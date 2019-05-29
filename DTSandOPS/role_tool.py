__author__ = "stefanotuv"
from DTSandOPS import db

class Role_Tool(db.Model):
    __tablename__ = "roles_tools"
    # role_tool_id = db.Column(db.Integer, primary_key=True)
    tool_id = db.Column(db.Integer, db.ForeignKey('tool.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    columns = ['tool_id', 'role_id']
