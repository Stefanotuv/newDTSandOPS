__author__ = "stefanotuv"

from flask_wtf import FlaskForm
from wtforms import SelectField,  StringField, PasswordField, SubmitField, BooleanField,FileField, validators


class RoleSelectionForm(FlaskForm):
    discipline = SelectField('discipline', choices=[])
    core_role = SelectField('core_role', choices=[])
    role = SelectField('role', choices=[])
    country = SelectField('country', choices=[])
    user_name = StringField('user_name')
    user_id = StringField('user_id',[validators.Length(min=8, max=8)])

class UserForm(FlaskForm):
    country = SelectField('country', choices=[])
    user_name = StringField('user_name')
    user_id = StringField('user_id',[validators.Length(min=8, max=8)])



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