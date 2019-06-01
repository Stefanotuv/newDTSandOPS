__author__ = "stefanotuv"

from flask_wtf import FlaskForm
from wtforms import SelectField,  StringField, PasswordField, FileField, validators


class SettingsDatabaseForm(FlaskForm):
    db_type = SelectField('role', choices=[])

class SettingsMysqlMongoForm(FlaskForm):
    host = StringField('host')
    db_name  = StringField('db_name')
    port = StringField('port')
    user_name = StringField('user_name')
    password = PasswordField('password')


class SettingsSqliteForm(FlaskForm):
    filename = FileField()