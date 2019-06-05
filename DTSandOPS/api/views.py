__author__ = "stefanotuv"

from DTSandOPS.main.models.tool_ad import Tool_AD
from DTSandOPS.main.models.tool import Tool
from DTSandOPS.main.models.role_tool import Role_Tool
from DTSandOPS.main.models.country import Country
from DTSandOPS.main.models.role import Role

from flask import Blueprint, jsonify

api_db = Blueprint('api_db', __name__, template_folder='templates', url_prefix='/api')

@api_db.route('/tables/<table_name>', methods = ['GET'])
# return all values in a table
def tables(table_name):
    full_values = []
    full_values

    if(table_name=="tool"):
        [full_values.append({'tool_id': q.tool_id, 'tool_name': q.tool_name, 'tool_vendor': q.tool_vendor}) for q in Tool.query.all()]

    elif(table_name=="role"):
        [full_values.append({'role_id': q.role_id, 'discipline': q.discipline, 'core_role': q.core_role, 'role': q.role}) for q in Role.query.all()]

    elif(table_name=="role_tool"):
        temp = Role_Tool.query.all()
        [full_values.append({'role_id': q.role_id, 'tool_id': q.tool_id}) for q in temp]

    elif((table_name=="tool_AD") or (table_name=="tool_ad")):
        [full_values.append({'tool_id': q.tool_id, 'country_id': q.country_id, 'ad_group': q.ad_group, 'tool_name': q.tool_name, 'country_code': q.country_code}) for q in Tool_AD.query.all()]

    elif (table_name=="country"):
        [full_values.append({'country_id': q.country_id, 'country_name': q.country_name, 'country_code': q.country_code}) for q in Country.query.all()]
    else:
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