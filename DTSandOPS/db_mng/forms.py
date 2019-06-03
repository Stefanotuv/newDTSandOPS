__author__ = "stefanotuv"

from flask_wtf import FlaskForm
from wtforms import SelectField,  StringField, PasswordField, FileField, validators
from DTSandOPS.db_mng.utilities.local_variables import LOCAL_DB_FOLDER, ALLOWED_DB_EXTENSIONS
from os import listdir
from os.path import isfile, join
import fnmatch
import os





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
        self.existing_db.choices = [('Create New', 'Create New'),('Upload','Upload')]
        pass

    def save_config(self):
        # get the data from the form and save in the json file: db_config.json
        pass

    def laod_db_settings(self):
        pass



class SettingsSqliteForm(FlaskForm):
    filename = FileField()
    existing_db = SelectField('existing_db', choices=[])

    # initialise the list  with the existing db in the folder
    def __init__(self):
        # get all the file .sql or .db from the folder
        super().__init__()
        self.existing_db.choices = [('New Connection', 'New Connection')]
        # load db file for option selection
        [self.existing_db.choices.append((item,item)) for item in self.laod_db_files()]
        pass

    def laod_db_files(self):
        # load files form the default folder
        db_sqlite_files = []
        for file in os.listdir(LOCAL_DB_FOLDER):
            if os.path.splitext(file)[1] in ALLOWED_DB_EXTENSIONS:
                db_sqlite_files.append(file)
                print(file)
        return db_sqlite_files