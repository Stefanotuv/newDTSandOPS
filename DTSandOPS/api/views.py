__author__ = "stefanotuv"

from DTSandOPS.main.models.tool_ad import Tool_AD
from DTSandOPS.main.models.tool import Tool
from DTSandOPS.main.models.role_tool import Role_Tool
from DTSandOPS.main.models.country import Country
from DTSandOPS.main.models.role import Role

from sqlalchemy.sql.expression import or_, and_
from DTSandOPS.utilities.global_variable import *
from werkzeug import secure_filename
from flask import current_app as app
import sys, os
import json
from flask import jsonify
from DTSandOPS.db_mng.views import db_mng
from sqlalchemy_utils import database_exists
from sqlalchemy import *
from DTSandOPS import db


from flask import Blueprint, jsonify, request

api_db = Blueprint('api_db', __name__, template_folder='templates', url_prefix='/api')

@api_db.route('/query/tables/<table_name>', methods=['GET'])
# return all values in a table
def query_tables(table_name):
    full_values = []

    if (table_name == "tool"):
        [full_values.append({'tool_id': q.tool_id, 'tool_name': q.tool_name, 'tool_vendor': q.tool_vendor}) for q in
         Tool.query.all()]

    elif (table_name == "role"):
        [full_values.append(
            {'role_id': q.role_id, 'discipline': q.discipline, 'core_role': q.core_role, 'role': q.role}) for q in
         Role.query.all()]

    elif (table_name == "role_tool"):
        temp = Role_Tool.query.all()
        [full_values.append({'role_id': q.role_id, 'tool_id': q.tool_id}) for q in temp]

    elif ((table_name == "tool_AD") or (table_name == "tool_ad")):
        [full_values.append(
            {'tool_id': q.tool_id, 'country_id': q.country_id, 'ad_group': q.ad_group, 'tool_name': q.tool_name,
             'country_code': q.country_code}) for q in Tool_AD.query.all()]

    elif (table_name == "country"):
        [full_values.append(
            {'country_id': q.country_id, 'country_name': q.country_name, 'country_code': q.country_code}) for q in
         Country.query.all()]

    else:
        return jsonify({"message": "table selected not available"})
        pass

    json_full_values = jsonify(full_values)
    # print(json_full_values)

    return json_full_values

@api_db.route('/query/disciplines', methods = ['GET'])
# return all the discipline in the table
def query_discipline():
    query = [(q.discipline, q.discipline) for q in Role.query.with_entities(Role.discipline).distinct(Role.discipline)]
    # return jsonify(query)
    return query
    pass

@api_db.route('/query/core_roles/<discipline>', methods=['GET'])
# return all the core_roles for a given discipline
def query_macro_role(discipline):
    query = [(q.core_role, q.core_role) for q in \
    Role.query.filter_by(discipline=discipline).with_entities(Role.core_role).distinct(Role.core_role)]
    return query
    pass

@api_db.route('/query/roles/<discipline>/<core_role>', methods=['GET'])
# return all the roles for a given core_role and discipline
def query_role(discipline,core_role):
    query = [(q.role, q.role) for q in \
            Role.query.filter_by(discipline=discipline, core_role=core_role).with_entities(Role.role).distinct(Role.role)]
    return query
    pass

@api_db.route('/query/countries', methods=['GET'])
# return all the roles for a given core_role and discipline
def query_countries():
    query = [(q.country_code, q.country_code) for q in \
                Country.query.with_entities(Country.country_code)]
    return query
    pass

@api_db.route('/query/roleid/<discipline>/<core_role>/<role>', methods=['GET'])
def query_roleid(discipline, core_role, role):
    query = [ q.role_id for q in Role.query.filter_by(discipline=discipline,core_role = core_role, role = role).with_entities(Role.role_id)]
    return query
    pass

# toolsIds
@api_db.route('/query/tool_id/<role_id>', methods=['GET'])
def query_toolid(role_id):
    query = [q.tool_id for q in Role_Tool.query.filter_by(role_id=role_id).with_entities(Role_Tool.tool_id)]
    return query
    pass


# detailed database query
@api_db.route('/query_and', methods=['POST'])
def query_main_and():

    # this query receive a Json to create any type of query to the db on the back-end

    # test if the request is json
    # if yes get the corresponding query from the json data if not return invalid message

    if request.is_json:

        if request.json['query_type'] is not None:
            query_type = request.json['query_type']
        else:
            query_type = None

        if request.json['table_name'] is not None:
            table_name = request.json['table_name']
        else:
            table_name = None

        if request.json['filters'] is not None:
            filters = request.json['filters']
        else:
            filters = None

        if request.json['output'] is not None:
            output = request.json['output']
        else:
            output = None

        if request.json['distinct'] is not None:
            distinct = request.json['distinct']
        else:
            distinct = None

        return query_tables_generic_and(table_name, filters, output ,
                                         distinct)

    else:
        return "not valid json request"

    pass

def query_tables_generic_and(table_name, columns_filters,columns_entities,columns_distinct):
    # to add: verify if the table exist to avoid errors

    # parameters for the queries
    full_values= []
    filters= []
    entities= []
    distinct = []

    if columns_filters is not None:
        [filters.append(getattr(getattr(sys.modules[__name__], table_name), list(item.keys())[0]) == (list(item.values())[0]))
         for item in columns_filters]

    if columns_entities is not None:
        [entities.append(getattr(getattr(sys.modules[__name__], table_name), item))
         for item in columns_entities]

    if columns_distinct is not None:
        [distinct.append(getattr(getattr(sys.modules[__name__], table_name), item))
         for item in columns_distinct]

    # prepare the query
    # the query is different based on with entities. if entities is None, the query wont select nay column
    if columns_entities is not None:
        que = getattr(sys.modules[__name__], table_name).query.filter(and_(*filters)).with_entities(*entities).distinct(*distinct)
        # create the output only for the entities columns
        for q in que:
            dict = {}
            for ent in getattr(sys.modules[__name__], table_name).columns:
                if ent in columns_entities:
                    dict[str(ent)] = getattr(q,str(ent))
            full_values.append(dict)
    else:
        que = getattr(sys.modules[__name__], table_name).query.filter(and_(*filters)).distinct(*distinct)
        # create the output for all columns
        for q in que:
            dict = {}
            for ent in getattr(sys.modules[__name__], table_name).columns:
                # dict[str(ent)] = q.ent
                dict[str(ent)] = getattr(q,str(ent))
            full_values.append(dict)

    json_full_values = json.dumps(full_values)
    return json_full_values

@api_db.route('/query_or', methods=['POST'])
def query_main_or():

    # this query receive a Json to create any type of query to the db on the back-end

    # test if the request is json
    # if yes get the corresponding query from the json data if not return invalid message

    if request.is_json:

        if request.json['query_type'] is not None:
            query_type = request.json['query_type']
        else:
            query_type = None

        if request.json['table_name'] is not None:
            table_name = request.json['table_name']
        else:
            table_name = None

        if request.json['filters'] is not None:
            filters = request.json['filters']
        else:
            filters = None

        if request.json['output'] is not None:
            output = request.json['output']
        else:
            output = None

        if request.json['distinct'] is not None:
            distinct = request.json['distinct']
        else:
            distinct = None

        # if query_type == "info":
        #     return query_tables_info(table_name)
        # elif query_type == "generic":
            return query_tables_generic_or(table_name, filters, output ,
                                         distinct)
        # else:
        #     pass

    else:
        return "not valid json request"

    pass

def query_tables_generic_or(table_name, columns_filters,columns_entities,columns_distinct):
    # to add: verify if the table exist to avoid errors

    # parameters for the queries
    full_values= []
    filters= []
    entities= []
    distinct = []

    if columns_filters is not None:
        [filters.append(getattr(getattr(sys.modules[__name__], table_name), list(item.keys())[0]) == (list(item.values())[0]))
         for item in columns_filters]

    if columns_entities is not None:
        [entities.append(getattr(getattr(sys.modules[__name__], table_name), item))
         for item in columns_entities]

    if columns_distinct is not None:
        [distinct.append(getattr(getattr(sys.modules[__name__], table_name), item))
         for item in columns_distinct]

    # prepare the query
    # the query is different based on with entities. if entities is None, the query wont select nay column
    if columns_entities is not None:
        que = getattr(sys.modules[__name__], table_name).query.filter(or_(*filters)).with_entities(*entities).distinct(*distinct)
        # create the output only for the entities columns
        for q in que:
            dict = {}
            for ent in getattr(sys.modules[__name__], table_name).columns:
                if ent in columns_entities:
                    dict[str(ent)] = getattr(q,str(ent))
            full_values.append(dict)
    else:
        que = getattr(sys.modules[__name__], table_name).query.filter(or_(*filters)).distinct(*distinct)
        # create the output for all columns
        for q in que:
            dict = {}
            for ent in getattr(sys.modules[__name__], table_name).columns:
                # dict[str(ent)] = q.ent
                dict[str(ent)] = getattr(q,str(ent))
            full_values.append(dict)

    json_full_values = json.dumps(full_values)
    return json_full_values

@api_db.route('/query_info', methods=['POST'])
def query_info():
    if request.is_json:

        # if request.json['query_type'] is not None:
        #     query_type = request.json['query_type']
        # else:
        #     query_type = None

        if request.json['table_name'] is not None:
            table_name = request.json['table_name']
        else:
            table_name = None

        return query_tables_info(table_name)

def query_tables_info(table_name):
    # to add: verify if the table exist to avoid errors

    # prepare the query
    # the query is different based on with entities. if entities is None, the query wont select nay column

    que = (getattr(sys.modules[__name__], table_name)).columns
    # que = Tool.columns

    json_full_values = json.dumps(que)
    return json_full_values


@api_db.route('/db_connect', methods=['POST'])
def db_connect():

    if request.is_json:

        if request.json['db_type'] is not None:
            db_type = request.json['db_type']
        else:
            db_type = None

        if request.json['host'] is not None:
            host = request.json['host']
        else:
            host = None

        if request.json['port'] is not None:
            port = request.json['port']
        else:
            port = None

        if request.json['db_name'] is not None:
            db_name = request.json['db_name']
        else:
            db_name = None

        if request.json['user'] is not None:
            user = request.json['user']
        else:
            user = None

        if request.json['psw'] is not None:
            psw = request.json['psw']
        else:
            psw = None

        if request.json['filename'] is not None:
            filename = request.json['filename']
        else:
            filename = None

    return connect_to_db(db_type,host,port,db_name,user,psw, filename)

    pass

def connect_to_db(db_type,host,port,db_name,user,psw,filename):
    if db_type == 'sqlite':
        db_exist = set_sqlite(filename)

    elif db_type == 'mysql':
        db_exist = set_mysql(host,port,db_name,user,psw)
        value = 'false'
        if db_exist == 'true':
            tables_exist = db.engine.table_names()
            table_list = TABLE_LIST
            value = 'false'
            for item in table_list:
                value = 'true' # required as the list can be empty
                if item in tables_exist:
                    pass
                else:
                    value = 'false' # if any of table is not present

        save_db_connection()

        return value



    elif db_type == 'mongo':
        db_exist = set_mongo(host,port,db_name,user,psw)

    elif db_type == 'postgress':
        pass
    else:
        # error?
        pass
    return db_exist

def check_db():
    # check if the db and the tables exist otherwise return an error


    pass

@api_db.route('/db_save', methods=['POST'])
def db_save():
    pass

def save_db_connection():
    # check the file exists
    # if the file exist import
    # append the configuration as a standard json-file
    load_db_connections()



    pass

@api_db.route('/db_load/<db_type>', methods=['GET','POST'])
def db_load(db_type,existing_db):
    json_data = load_db_connections()

    if db_type == 'mongo':

        jreturn = jsonify(json_data['mongo'])

    elif db_type =='mysql':

        jreturn = jsonify(json_data['mysql'])
    else:
        jreturn = jsonify(json_data)

    return jreturn

@api_db.route('/db_load', methods=['GET','POST'])
def db_load_all():
    json_data = load_db_connections()
    jreturn = jsonify(json_data)

    return jreturn

def load_db_connections():
    # check if file exist

    file = os.path.join(UPLOAD_INITIATE_FOLDER, DATABASE_FILE_CONNECTIONS)

    print(file)
    if os.path.isfile(file):
        json_db_connection = loadjson(file)
        pass
    else:
        pass

    return json_db_connection

def loadjson(filename):

    '''read Json from file'''

    with open(filename, 'r') as f:
        json_data = json.load(f)
    return json_data

def set_sqlite(filename):


    file = request.files['filename']
    filename = secure_filename(file.filename)
    app.config['LOCAL_DB_FOLDER'] = LOCAL_DB_FOLDER
    file.save(os.path.join(app.config['LOCAL_DB_FOLDER'], filename))
    allowed = allowed_file(filename)
    if ((filename != "") and (allowed == True)):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['LOCAL_DB_FOLDER'], filename)
        app.config['dbtype'] = 'sqlite'

        app.config['connected'] = True
        # return the tables in the connected db


    return 'true'


def set_mysql(host,port,db_name,user,psw):

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'. \
        format(user, psw, \
               host, port,
               db_name)
    app.config['dbtype'] = 'mysql'

    if database_exists(db.engine.url):
        app.config['connected'] = True
        return 'true'
    else:
        app.config['connected'] = False
        return 'false'

    return 'false'

def set_mongo(host,port,db_name,user,psw):

        # location fo the db, dbname, user and password to be passed as parameter

    app.config['MONGOALCHEMY_DATABASE'] = db_name
    app.config['MONGOALCHEMY_SERVER'] = host
    app.config['MONGOALCHEMY_PORT'] = port
    app.config['MONGOALCHEMY_USER'] = user
    app.config['MONGOALCHEMY_PASSWORD'] = psw
    app.config['dbtype'] = 'mongo'
    app.config['connected'] = True

    return 'True'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS