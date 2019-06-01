__author__ = "stefanotuv"
from DTSandOPS import db

class Tool_AD(db.Model):
        __tablename__ = "Tool_AD"
        # role_tool.py = db.Column(db.Integer, primary_key=True)
        tool_id = db.Column(db.Integer, db.ForeignKey('tool.tool_id'),  primary_key=True)
        country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'),  primary_key=True)
        tool_name = db.Column(db.String(25), db.ForeignKey('tool.tool_name'),  primary_key=True)
        country_code = db.Column(db.String(3), db.ForeignKey('country.country_code'),  primary_key=True)
        ad_group = db.Column(db.String(50))
        columns = ['tool_id', 'country_id', 'tool_name','country_code','ad_group']
