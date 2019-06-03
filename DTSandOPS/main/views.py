__author__ = "stefanotuv"

from flask import request, render_template, jsonify, Blueprint, url_for
from DTSandOPS.main.models.role import Role
from DTSandOPS.main.models.role_tool import Role_Tool
from DTSandOPS.main.models.tool_ad import Tool_AD
from DTSandOPS.main.models.tool import Tool
from DTSandOPS.main.models.country import Country
from DTSandOPS.main.forms import RoleSelectionForm, UserForm
from flask import current_app as app

from DTSandOPS.utilities.global_variable import *

main = Blueprint('main', __name__, template_folder='templates', url_prefix='/main')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/main_page', methods = ['GET', 'POST'])
def main_page():
    role_selection_form = RoleSelectionForm()
    user_form = UserForm()
    # login_manager = LoginManager()
    Json_users_data = ''
    json_user_table = ''
    full_tool_values = [q for q in Tool.query.all()]
    full_tool_array = []
    [full_tool_array.append({'id': tool.tool_id, 'name': tool.tool_name, 'vendor': tool.tool_vendor}) \
     for tool in full_tool_values]

    # this is the intialisation of the page.
    # The initial value are for the first option on the Discipline
    if request.method == 'POST':


        keys = [key for key in request.form.keys()]
        value_selected = [request.form[key] for key in keys]
        Json_users_data = app.config['user_table']


        # the file for the table requires only the ID country and role a function to be created
        json_user_table = Json_users_data_reduced(Json_users_data)


        roleId = [ q.role_id for q in Role.query.filter_by(discipline=value_selected[1],core_role = value_selected[2], role = value_selected[3]).with_entities(Role.role_id)]
        toolsIds = [ q.tool_id for q in Role_Tool.query.filter_by(role_id=roleId[0]).with_entities(Role_Tool.tool_id)]
        tool_values = [ q for q in Tool.query.filter(Tool.tool_id.in_(toolsIds))]
        column_name = Tool.columns
        tool_array = []
        [tool_array.append({'id': tool.tool_id, 'name': tool.tool_name, 'vendor': tool.tool_vendor })\
                            for tool in tool_values]


        jsondata = {'column_name': column_name, 'tools': tool_array, 'full_tools': full_tool_array, 'selected': value_selected[1:] }


        role_selection_form.discipline.choices = [(q.discipline, q.discipline) for q in \
            Role.query.with_entities(Role.discipline).distinct(Role.discipline)]

        # role_selection_form.discipline.choices = url_for('/query/roles/disciplines')

        role_selection_form.core_role.choices = [(q.core_role, q.core_role) for q in \
            Role.query.filter_by(discipline=value_selected[1]). \
                    with_entities(Role.core_role).distinct(Role.core_role)]

        # role_selection_form.core_role.choices = url_for('/query/core_roles/<{}'.format(value_selected[1]))

        role_selection_form.role.choices = [(q.role, q.role) for q in \
            Role.query.filter_by(discipline=value_selected[1], \
                core_role=value_selected[2]). \
                    with_entities(Role.role).distinct(Role.role)]

        # role_selection_form.role.choices = url_for('/query/roles/{}/{}'.format(value_selected[1],value_selected[2]))

        user_form.country.choices = [(q.country_code, q.country_code) for q in \
            Country.query.with_entities(Country.country_code)]

        # return render_template('main_page_new_10_1.html', form= role_selection_form, user_form=user_form, jsondata=jsondata, json_user_table=json_user_table)

    else:

        role_selection_form.discipline.choices = [(q.discipline, q.discipline) for q in \
            Role.query.with_entities(Role.discipline).distinct(Role.discipline)]

        role_selection_form.core_role.choices = [(q.core_role, q.core_role) for q in \
            Role.query.filter_by(discipline = role_selection_form.discipline.choices[0][0]).\
                with_entities(Role.core_role).distinct(Role.core_role)]

        role_selection_form.role.choices = [(q.role, q.role) for q in \
            Role.query.filter_by(discipline = role_selection_form.discipline.choices[0][0], \
                core_role = role_selection_form.core_role.choices[0][0]).\
                    with_entities(Role.role).distinct(Role.role)]

        user_form.country.choices = [(q.country_code, q.country_code) for q in \
            Country.query.with_entities(Country.country_code)]

        # add the initial values to the table --------------------------------------------
        toolsIds = [ q.tool_id for q in Role_Tool.query.filter_by(role_id=1).with_entities(Role_Tool.tool_id)]
        tool_values = [ q for q in Tool.query.filter(Tool.tool_id.in_(toolsIds))]
        column_name = Tool.columns
        tool_array = []
        [tool_array.append({'id': tool.tool_id, 'name': tool.tool_name, 'vendor': tool.tool_vendor })\
                            for tool in tool_values]
        jsondata = {'column_name': column_name, 'tools': tool_array, 'full_tools': full_tool_array, 'selected': [] }
        #----------------------------------------------------------------------------------------

    return render_template('main_page_new_11.html', form = role_selection_form, user_form=user_form, jsondata=jsondata, json_user_table= json_user_table)

@main.route('/core_role/<discipline_selected>')
# used to load the core_role and role based on the discipline selected
def core_role_load(discipline_selected):

    core_role = Role.query.filter_by(discipline = discipline_selected).\
        with_entities(Role.core_role).distinct(Role.core_role)

    core_role_array = []

    [core_role_array.append({'id':cr.core_role,'name':cr.core_role}) for cr in core_role]

    role = Role.query.filter_by(discipline=discipline_selected, core_role=core_role_array[0]['name']). \
                with_entities(Role.role).distinct(Role.role)

    role_array = []

    [role_array.append({'id': rol.role, 'name': rol.role}) for rol in role]

    return jsonify({'core_role' : core_role_array, 'role': role_array})

@main.route('/role/<discipline_selected>/<core_role_selected>')
# used to load the role based on the core_role selected
def role_load(discipline_selected,core_role_selected):

    role = Role.query.filter_by(discipline=discipline_selected, core_role=core_role_selected). \
                with_entities(Role.role).distinct(Role.role)
    role_array = []
    [role_array.append({'id': rol.role, 'name': rol.role}) for rol in role]

    return jsonify({'role': role_array})

@main.route('/tool_AD/<tool>/<country>')
# used to extract the AD for the tool based on the country
def tool_AD_for_country(tool,country):

    tool_ad = Tool_AD.query.filter_by(tool_name=tool, country_code=country). \
                with_entities(Tool_AD.ad_group)

    tool_ad_array = []
    [tool_ad_array.append({'ad_group': ad.ad_group}) for ad in tool_ad]

    print(jsonify({'ad_group': tool_ad_array}))
    return jsonify({'ad_group': tool_ad_array})

# record the table of users
@main.route('/user_table', methods = ['GET', 'POST'])
def store_user_table():
    if request.method == 'POST':
        app.config['user_table'] = request.json
        # print(request.json)
    elif request.method == 'GET':
        data = jsonify(app.config['user_table'])
        # print(data)
        return data
    else:
        pass
    return ''

@main.route('/tables/<table_name>', methods = ['GET'])
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

    elif(table_name=="tool_AD"):
        [full_values.append({'tool_id': q.tool_id, 'country_id': q.country_id, 'ad_group': q.ad_group, 'tool_name': q.tool_name, 'country_code': q.country_code}) for q in Tool_AD.query.all()]

    elif (table_name=="country"):
        [full_values.append({'country_id': q.country_id, 'country_name': q.country_name, 'country_code': q.country_code}) for q in Country.query.all()]
    else:
        pass
    json_full_values = jsonify(full_values)

    print(json_full_values)

    return json_full_values
    pass


def Json_users_data_reduced(Json_data_list):
    Json_reduced = []

    [Json_reduced.append({'id' : 'id', 'user_id': Json_data['user_id'], 'role': Json_data['role'], 'country': Json_data['country']}) for Json_data in Json_data_list]

    return Json_reduced
