__author__ = "stefanotuv"

from DTSandOPS.main.models.tool_ad import Tool_AD
from DTSandOPS.main.models.tool import Tool
from DTSandOPS.main.models.role_tool import Role_Tool
from DTSandOPS.main.models.country import Country
from DTSandOPS.main.models.role import Role
from sqlalchemy.sql.expression import or_, and_

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

# @api_db.route('/query/tool_values/<tool_ids>', methods=['GET'])
# def query_toolid(tool_ids):
#     query = [ q for q in Tool.query.filter(Tool.tool_id.in_(tool_ids))]
#     return query
#     pass

@api_db.route('/query', methods=['POST'])

def query_generic():

    # this query receive a Json to create any type of query to the db on the back-end

    # test if the request is json
    # if yes get the corresponding query from the json data if not return invalid message

    if request.is_json:
        # elaborate the json data
        query_type = request.json['query_type']

        if query_type == "select_all_from_table":
            # TO ADD: check if the other fields in the query are empty
            return query_tables_all(request.json['table_name'])

            pass
        elif query_type == "select_filtered":
            # TO ADD: check if the filter is not field in the query are empty

            return query_tables_filtered(request.json['table_name'], request.json['filters'])

            pass

        elif query_type == "select_return":
            pass

        elif query_type == "select_filtered_return":
            return query_tables_filtered_entities_distinct(request.json['table_name'], request.json['filters'], request.json['output'],
                                         request.json['distinct'])

            pass

        else :
            return "not valid json query request"
            pass

        pass
    else:
        return "not valid json request"


    pass


# detailed database query

def query_tables_all(table_name):
    full_values = []

    if (table_name == "tool"):
        [full_values.append({'tool_id': q.tool_id, 'tool_name': q.tool_name, 'tool_vendor': q.tool_vendor}) for q in
         Tool.query.all()]

    elif (table_name == "role"):
        [full_values.append(
            {'role_id': q.role_id, 'discipline': q.discipline, 'core_role': q.core_role, 'role': q.role}) for q in
         Role.query.all()]

    elif (table_name == "role_tool"):
        [full_values.append({'role_id': q.role_id, 'tool_id': q.tool_id}) for q in Role_Tool.query.all()]

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

def query_tables_filtered(table_name, columns_filters):
    full_values = []
    filters = []

    for item in columns_filters:
        key = list(item.keys())[0]
        value = list(item.values())[0]


    if (table_name == "tool"):
        # que = Tool.query.filter(Tool.__getattribute__(Tool,key)==value)
        que = Tool.query.filter(getattr(Tool, key) == value)
        [full_values.append({'tool_id': q.tool_id, 'tool_name': q.tool_name, 'tool_vendor': q.tool_vendor}) for q in
         que]

    elif (table_name == "role"):
        # que = Role.query.filter(Role.__getattribute__(Role, key) == value)
        for item in columns_filters:
            filters.append(getattr(Role, list(item.keys())[0]) == (list(item.values())[0]))

        que = Role.query.filter(and_(*filters))
        # que = Role.query.filter(getattr(Role, key) == value)
        [full_values.append(
            {'role_id': q.role_id, 'discipline': q.discipline, 'core_role': q.core_role, 'role': q.role}) for q in
         que]

    elif (table_name == "role_tool"):
        # que = Role_Tool.query.filter(Role_Tool.__getattribute__(Role_Tool, key) == value)
        que = Role_Tool.query.filter(getattr(Role_Tool, key) == value)
        [full_values.append({'role_id': q.role_id, 'tool_id': q.tool_id}) for q in que]

    elif ((table_name == "tool_AD") or (table_name == "tool_ad")):
        # que = Tool_AD.query.filter(Tool_AD.__getattribute__(Tool_AD, key) == value)
        que = Tool_AD.query.filter(getattr(Tool_AD, key) == value)
        [full_values.append(
            {'tool_id': q.tool_id, 'country_id': q.country_id, 'ad_group': q.ad_group, 'tool_name': q.tool_name,
             'country_code': q.country_code}) for q in que]

    elif (table_name == "country"):
        # que = Country.query.filter(Country.__getattribute__(Country, key) == value)
        que = Country.query.filter(getattr(Country, key) == value)
        [full_values.append(
            {'country_id': q.country_id, 'country_name': q.country_name, 'country_code': q.country_code}) for q in
                que]

    else:
        return jsonify({"message": "table selected not available"})
        pass

    json_full_values = jsonify(full_values)
    # print(json_full_values)

    return json_full_values

def query_tables_filtered_entities_distinct(table_name, columns_filters,column_entities,column_distinct):
    full_values = []
    filters = []
    entities = []
    distinct = []

    for item in columns_filters:
        key = list(item.keys())[0]
        value = list(item.values())[0]


    if (table_name == "tool"):
        # que = Tool.query.filter(Tool.__getattribute__(Tool,key)==value)
        que = Tool.query.filter(getattr(Tool, key) == value)
        [full_values.append({'tool_id': q.tool_id, 'tool_name': q.tool_name, 'tool_vendor': q.tool_vendor}) for q in
         que]

    elif (table_name == "role"):
        # que = Role.query.filter(Role.__getattribute__(Role, key) == value)
        for item in columns_filters:
            filters.append(getattr(Role, list(item.keys())[0]) == (list(item.values())[0]))

        if column_entities is not None:
            for item in column_entities:
                entities.append(getattr(Role,item))
                pass
        if column_distinct is not None:
            for item in column_distinct:
                distinct.append(getattr(Role, item))
                pass

        que = Role.query.filter(and_(*filters)).with_entities(*entities).distinct(*distinct)
        # que = Role.query.filter(getattr(Role, key) == value)
        [full_values.append(
            {'role_id': q.role_id, 'discipline': q.discipline, 'core_role': q.core_role, 'role': q.role}) for q in
         que]

    elif (table_name == "role_tool"):
        # que = Role_Tool.query.filter(Role_Tool.__getattribute__(Role_Tool, key) == value)
        que = Role_Tool.query.filter(getattr(Role_Tool, key) == value)
        [full_values.append({'role_id': q.role_id, 'tool_id': q.tool_id}) for q in que]

    elif ((table_name == "tool_AD") or (table_name == "tool_ad")):
        # que = Tool_AD.query.filter(Tool_AD.__getattribute__(Tool_AD, key) == value)
        que = Tool_AD.query.filter(getattr(Tool_AD, key) == value)
        [full_values.append(
            {'tool_id': q.tool_id, 'country_id': q.country_id, 'ad_group': q.ad_group, 'tool_name': q.tool_name,
             'country_code': q.country_code}) for q in que]

    elif (table_name == "country"):
        # que = Country.query.filter(Country.__getattribute__(Country, key) == value)
        que = Country.query.filter(getattr(Country, key) == value)
        [full_values.append(
            {'country_id': q.country_id, 'country_name': q.country_name, 'country_code': q.country_code}) for q in
                que]

    else:
        return jsonify({"message": "table selected not available"})
        pass

    json_full_values = jsonify(full_values)
    # print(json_full_values)

    return json_full_values

