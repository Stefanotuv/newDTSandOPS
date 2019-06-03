__author__ = "stefanotuv"


from flask import request, render_template, jsonify, Blueprint
from DTSandOPS.db_mng.forms import SettingsDatabaseForm, SettingsMysqlMongoForm, SettingsSqliteForm
from flask import current_app as app

from werkzeug import secure_filename
from DTSandOPS.utilities.global_variable import *
from DTSandOPS.db_mng.utilities.local_variables import *
from DTSandOPS import db


db_mng = Blueprint('db_mng', __name__, template_folder='templates', url_prefix='/db')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@db_mng.route('/connect', methods = ['GET', 'POST'])
    # this should be used to configure the DB to be used
def connect():
    settingsDBForm = SettingsDatabaseForm()
    settingsDBForm.db_type.choices = [('mysql', 'mysql'), ('sqlite', 'sqlite'),  ('mongo', 'mongo')]

    settingsMysqlMongoForm = SettingsMysqlMongoForm()
    settingsSqliteForm = SettingsSqliteForm()
    jsondata={}

    if request.method == 'POST':
    # getting the information from the post to get what DB and the other
    # connectivity details

        keys = [key for key in request.form.keys()]
        value_selected = [request.form[key] for key in keys]

        db_type = value_selected[1]
        jsondata ={'selected':db_type}
        if db_type == 'sqlite':
            file = request.files['filename']
            filename = secure_filename(file.filename)
            app.config['LOCAL_DB_FOLDER'] = LOCAL_DB_FOLDER
            file.save(os.path.join(app.config['LOCAL_DB_FOLDER'], filename))
            allowed = allowed_file(filename)
            if ((filename != "") and (allowed == True)):
                app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['LOCAL_DB_FOLDER'], filename)
                app.config['dbtype'] = 'sqlite'
                app.config['connected'] = True

                # db_tables


                return render_template('connected.html')
            else:
                app.config['dbtype'] = ''
                app.config['connected'] = False

                pass


        elif db_type == 'mysql':
            if ((settingsMysqlMongoForm.host.data != "") and (settingsMysqlMongoForm.db_name.data != "")\
                    and (settingsMysqlMongoForm.user_name.data != "") and (settingsMysqlMongoForm.port.data != "") and (settingsMysqlMongoForm.password.data != "")):
                # location fo the db, dbname, user and password to be passed as parameter
                app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.\
                    format(settingsMysqlMongoForm.user_name.data,settingsMysqlMongoForm.password.data,\
                           settingsMysqlMongoForm.host.data,settingsMysqlMongoForm.port.data,settingsMysqlMongoForm.db_name.data)
                app.config['dbtype'] = 'mysql'
                app.config['connected'] = True
                return render_template('connected.html')
            else:
                app.config['dbtype'] = ''
                app.config['connected'] = False
        elif db_type == 'mongo':
            if ((settingsMysqlMongoForm.host.data != "") and (settingsMysqlMongoForm.db_name.data != "")\
                    and (settingsMysqlMongoForm.user_name.data != "") and (settingsMysqlMongoForm.port.data != "") and (settingsMysqlMongoForm.password.data != "")):
            # location fo the db, dbname, user and password to be passed as parameter

                app.config['MONGOALCHEMY_DATABASE'] = settingsMysqlMongoForm.db_name.data
                app.config['MONGOALCHEMY_SERVER'] = settingsMysqlMongoForm.host.data
                app.config['MONGOALCHEMY_PORT'] = settingsMysqlMongoForm.port.data
                app.config['MONGOALCHEMY_USER'] = settingsMysqlMongoForm.user_name.data
                app.config['MONGOALCHEMY_PASSWORD'] = settingsMysqlMongoForm.password.data
                app.config['dbtype'] = 'mongo'
                app.config['connected'] = True
                return render_template('connected.html')
            else:
                app.config['dbtype'] = ''
                app.config['connected'] = False
        elif db_type == 'postgress':
            pass
        else:
            # error?
            pass

    else:
        return render_template('config.html', formDB=settingsDBForm, formMysqlMongo=settingsMysqlMongoForm, formSqlite=settingsSqliteForm, jsondata=jsondata)
        pass

    return render_template('config.html', formDB=settingsDBForm, formMysqlMongo=settingsMysqlMongoForm, formSqlite=settingsSqliteForm, jsondata=jsondata)

@db_mng.route('/check_connection')
# check if the connection is active
# connections apply only for
def check_connection():
    pass

@db_mng.route('/check_table')
# check if the table exist in the db
def check_table():
    pass


def Json_users_data_reduced(Json_data_list):
    Json_reduced = []

    [Json_reduced.append({'id' : 'id', 'user_id': Json_data['user_id'], 'role': Json_data['role'], 'country': Json_data['country']}) for Json_data in Json_data_list]

    return Json_reduced
