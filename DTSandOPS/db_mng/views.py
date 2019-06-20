__author__ = "stefanotuv"


from flask import request, render_template, jsonify, Blueprint
from DTSandOPS.db_mng.forms import SettingsDatabaseForm, SettingsMysqlMongoForm, SettingsSqliteForm
from flask import current_app as app
import requests
from sqlalchemy_utils import database_exists
from werkzeug import secure_filename
from DTSandOPS.utilities.global_variable import *
from DTSandOPS.db_mng.utilities.local_variables import *
from DTSandOPS import db
# from flask_sqlalchemy import database_exists

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

    # prepopulate forms with the datafile saved
    value_test = send_connect_data_get("http://127.0.0.1:5000/api/db_load_all")


    if request.method == 'POST':
    # getting the information from the post to get what DB and the other
    # connectivity details

        keys = [key for key in request.form.keys()]
        value_selected = [request.form[key] for key in keys]

        db_type = value_selected[1]
        jsondata ={'selected': db_type}
        if db_type == 'sqlite':
            file = request.files['filename'] if request.files['filename'] is not None else request.files['filename']
            filename = secure_filename(file.filename)
            created = send_connect_data_post("http://127.0.0.1:5000/api/db_connect", db_type='sqlite', host=None, port=None, db_name=None, user=None, psw=None,
                                   filename=filename)

            # verify the db contains the tables

            return render_template('connected.html')
        elif db_type == 'mysql':

            if ((settingsMysqlMongoForm.host.data != "") and (settingsMysqlMongoForm.db_name.data != "")\
                    and (settingsMysqlMongoForm.user_name.data != "") and (settingsMysqlMongoForm.port.data != "") and (settingsMysqlMongoForm.password.data != "")):
                    user = settingsMysqlMongoForm.user_name.data
                    psw = settingsMysqlMongoForm.password.data
                    host = settingsMysqlMongoForm.host.data
                    port =settingsMysqlMongoForm.port.data
                    db_name = settingsMysqlMongoForm.db_name.data
                    value = send_connect_data_post("http://127.0.0.1:5000/api/db_connect", db_type='mysql', host=host, port=port, db_name=db_name, user=user, psw=psw,
                                           filename=None)


                    if value == True:
                        return render_template('connected.html')
                    else:
                        return render_template('No-connected.html')
        elif db_type == 'mongo':
            if ((settingsMysqlMongoForm.host.data != "") and (settingsMysqlMongoForm.db_name.data != "")\
                    and (settingsMysqlMongoForm.user_name.data != "") and (settingsMysqlMongoForm.port.data != "") and (settingsMysqlMongoForm.password.data != "")):

                user = settingsMysqlMongoForm.user_name.data
                psw = settingsMysqlMongoForm.password.data
                host = settingsMysqlMongoForm.host.data
                port = settingsMysqlMongoForm.port.data
                db_name = settingsMysqlMongoForm.db_name.data
                send_connect_data_post("http://127.0.0.1:5000/api/db_connect", db_type='mongo', host=host, port=port,
                                       db_name=db_name, user=user, psw=psw,
                                       filename=None)
                return render_template('connected.html')
        elif db_type == 'postgress':
            pass
        else:
            # error?
            pass
        return render_template('config.html', formDB=settingsDBForm, formMysqlMongo=settingsMysqlMongoForm,
                           formSqlite=settingsSqliteForm, jsondata=jsondata)
    else:
        return render_template('config.html', formDB=settingsDBForm, formMysqlMongo=settingsMysqlMongoForm, formSqlite=settingsSqliteForm, jsondata=jsondata)
        pass






@db_mng.route('/check_tables')
# check if the table exist in the db
def check_tables():
    return [cls for cls in db.Model._decl_class_registry.values() if isinstance(cls, type) and issubclass(cls, db.Model)]
    pass


def Json_users_data_reduced(Json_data_list):
    Json_reduced = []

    [Json_reduced.append({'id' : 'id', 'user_id': Json_data['user_id'], 'role': Json_data['role'], 'country': Json_data['country']}) for Json_data in Json_data_list]

    return Json_reduced


def send_connect_data_post(api_address, db_type, host, port=None, db_name=None, user=None, psw=None,filename=None):

    json_query = {

        # options: info, generic
        "db_type": db_type,

        "host": host,

        "port": port,

        "db_name": db_name,

        "user": user,

        "psw" : psw,

        "filename" : filename
    }

    resp = requests.post(api_address, json=json_query)
    return resp.json()

def send_connect_data_get(api_address):


    resp = requests.get(api_address)
    return resp.json()
