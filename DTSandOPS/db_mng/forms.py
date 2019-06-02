__author__ = "stefanotuv"

from flask_wtf import FlaskForm
import os
from wtforms import SelectField,  StringField, PasswordField, FileField, validators
from DTSandOPS.db_mng.utilities.local_variables import LOCAL_DB_FOLDER

class SettingsDatabaseForm(FlaskForm):
    db_type = SelectField('role', choices=[])


class SettingsMysqlMongoForm(FlaskForm):
    host = StringField('host')
    db_name  = StringField('db_name')
    port = StringField('port')
    user_name = StringField('user_name')
    password = PasswordField('password')
    existing_db = SelectField('existing_db', choices=[])

    def __init__(self):
        # use a local json file where to save the connection details once they are successful
        super().__init__()
        self.existing_db.choices = [('Empty', 'Empty')]
        pass

    def save_config(self):
        # get the data from the form and save in the json file: db_config.json
        pass



class SettingsSqliteForm(FlaskForm):
    filename = FileField()
    existing_db = SelectField('existing_db', choices=[])

    # initialise the list  with the existing db in the folder

    def __init__(self):
        # get all the file .sql or .db from the folder
        super().__init__()
        self.existing_db.choices = [('Empty', 'Empty')]
        pass