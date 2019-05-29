__author__ = "stefanotuv"

from DTSandOPS import db

class Country(db.Model):
    __tablename__ = "countries"
    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(25))
    country_code = db.Column(db.String(3))
    columns = ['country_id', 'country_name', 'country_code']