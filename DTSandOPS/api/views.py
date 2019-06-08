__author__ = "stefanotuv"

from DTSandOPS.main.models.tool_ad import Tool_AD
from DTSandOPS.main.models.tool import Tool
from DTSandOPS.main.models.role_tool import Role_Tool
from DTSandOPS.main.models.country import Country
from DTSandOPS.main.models.role import Role
from sqlalchemy.sql.expression import or_, and_
import sys
import json

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


@api_db.route('/query', methods=['POST'])
def query_generic():

    # this query receive a Json to create any type of query to the db on the back-end

    # test if the request is json
    # if yes get the corresponding query from the json data if not return invalid message

    if request.is_json:

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

        return query_tables_generic(table_name, filters, output ,
                                         distinct)
    else:
        return "not valid json request"

    pass


# detailed database query
def query_tables_generic(table_name, columns_filters,columns_entities,columns_distinct):
    # to add: verify if the table exist to avoid errors

    # parameters for the queries
    full_values= []
    filters= []
    entities= []
    distinct = []

    if columns_filters is not None:
        [filters.append(
            getattr(getattr(sys.modules[__name__], table_name), list(item.keys())[0]) == (list(item.values())[0])) for item
         in columns_filters]

    if columns_entities is not None:
        [entities.append(getattr(getattr(sys.modules[__name__], table_name), item)) for item in columns_entities]

    if columns_distinct is not None:
        [distinct.append(getattr(getattr(sys.modules[__name__], table_name), item)) for item in columns_distinct]

    # prepare the query
    # the query is different based on with entities. if entities is None, the query wont select nay column
    if columns_entities is not None:
        que = getattr((sys.modules[__name__], table_name)).query.filter(and_(*filters)).with_entities(*entities).distinct(*distinct)
        # create the output only for the entities columns
        for q in que:
            dict = {}
            for ent in entities:
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
    # json_full_values = jsonify(full_values)
    # print(json_full_values)
    return json_full_values

def query_tables_generic_list(table_name, columns_filters,columns_entities,columns_distinct):
    # to add: verify if the table exist to avoid errors

    # parameters for the queries
    full_values= []
    filters= []
    entities= []
    distinct = []

    if columns_filters is not None:
        [filters.append(
            getattr(getattr(sys.modules[__name__], table_name), list(item.keys())[0]) == (list(item.values())[0])) for item
         in columns_filters]

    if columns_entities is not None:
        [entities.append(getattr(getattr(sys.modules[__name__], table_name), item)) for item in columns_entities]

    if columns_distinct is not None:
        [distinct.append(getattr(getattr(sys.modules[__name__], table_name), item)) for item in columns_distinct]

    # prepare the query
    # the query is different based on with entities. if entities is None, the query wont select nay column
    if columns_entities is not None:
        que = getattr((sys.modules[__name__], table_name)).query.filter(and_(*filters)).with_entities(*entities).distinct(*distinct)
        # create the output only for the entities columns
        for q in que:
            dict = {}
            for ent in entities:
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
    # return full_values
    json_full_values = jsonify(full_values)
    print(json_full_values)
    return json_full_values





