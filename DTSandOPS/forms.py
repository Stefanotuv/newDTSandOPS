__author__ = "stefanotuv"

from flask_wtf import FlaskForm
from wtforms import SelectField,  StringField, PasswordField, SubmitField, BooleanField,FileField, validators
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from DTSandOPS.user import User

class LoginForm(FlaskForm):
    # user_id = StringField('user_id',validators=[DataRequired()])
    # user_name = StringField('user_name',validators=[DataRequired(), Length(min=3, max=20)])
    # user_name = StringField('user_name')
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    # in the other forms the SubmitField was not included/ used
    submit = SubmitField('LogIn')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(LoginForm, self).__init__(*args, **kwargs)


class RegistrationForm(FlaskForm):
    # user_id = StringField('User_id', validators=[DataRequired()])
    user_name = StringField('User_name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    # in the other forms the SubmitField was not included/ used
    submit = SubmitField('Register')

    def validate_user_name(self, user_name):
        user = User.query.filter_by(user_name=user_name.data).first()
        if user is not None:
            raise ValidationError('Please use a diff erent username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(RegistrationForm, self).__init__(*args, **kwargs)

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