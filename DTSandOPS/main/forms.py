__author__ = "stefanotuv"

from flask_wtf import FlaskForm
from wtforms import SelectField,  StringField, validators


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

