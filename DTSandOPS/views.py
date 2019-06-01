__author__ = "stefanotuv"

from flask import request, render_template, jsonify, url_for, redirect
from DTSandOPS.user import User
from DTSandOPS.role import Role
from DTSandOPS.role_tool import Role_Tool
from DTSandOPS.tool_ad import Tool_AD
from DTSandOPS.tool import Tool
from DTSandOPS.country import Country
from DTSandOPS.forms import RoleSelectionForm, UserForm, RegistrationForm, LoginForm
from DTSandOPS.forms import SettingsDatabaseForm, SettingsMysqlMongoForm, SettingsSqliteForm
from DTSandOPS import app
from DTSandOPS import db

from werkzeug import secure_filename
from DTSandOPS.utils.global_variable import *
from flask_login import login_user, current_user, logout_user,current_user, login_required
from flask import flash

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/connect', methods = ['GET','POST'])
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
            file.save(os.path.join(app.config['LOCAL_DB_FOLDER'], filename))
            allowed = allowed_file(filename)
            if ((filename != "") and (allowed == True)):
                app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.config['LOCAL_DB_FOLDER'], filename)

            else:
                pass

        elif db_type == 'mysql':
            if ((settingsMysqlMongoForm.host.data != "") and (settingsMysqlMongoForm.db_name.data != "")\
                    and (settingsMysqlMongoForm.user_name.data != "") and (settingsMysqlMongoForm.port.data != "") and (settingsMysqlMongoForm.password.data != "")):
            # location fo the db, dbname, user and password to be passed as parameter
                app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.\
                    format(settingsMysqlMongoForm.user_name.data,settingsMysqlMongoForm.password.data,\
                           settingsMysqlMongoForm.host.data,settingsMysqlMongoForm.port.data,settingsMysqlMongoForm.db_name.data)
            else:
                pass
        elif db_type == 'mongo':
            if ((settingsMysqlMongoForm.host.data != "") and (settingsMysqlMongoForm.db_name.data != "")\
                    and (settingsMysqlMongoForm.user_name.data != "") and (settingsMysqlMongoForm.port.data != "") and (settingsMysqlMongoForm.password.data != "")):
            # location fo the db, dbname, user and password to be passed as parameter

                app.config['MONGOALCHEMY_DATABASE'] = settingsMysqlMongoForm.db_name.data
                app.config['MONGOALCHEMY_SERVER'] = settingsMysqlMongoForm.host.data
                app.config['MONGOALCHEMY_PORT'] = settingsMysqlMongoForm.port.data
                app.config['MONGOALCHEMY_USER'] = settingsMysqlMongoForm.user_name.data
                app.config['MONGOALCHEMY_PASSWORD'] = settingsMysqlMongoForm.password.data
            else:
                pass

        else:
            # error?
            pass
    else:
        pass

    return render_template('config.html', formDB=settingsDBForm, formMysqlMongo=settingsMysqlMongoForm, formSqlite=settingsSqliteForm, \
                           jsondata=jsondata)

@app.route('/main_page', methods = ['GET','POST'])
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

        role_selection_form.core_role.choices = [(q.core_role, q.core_role) for q in \
            Role.query.filter_by(discipline=value_selected[1]). \
                    with_entities(Role.core_role).distinct(Role.core_role)]

        role_selection_form.role.choices = [(q.role, q.role) for q in \
            Role.query.filter_by(discipline=value_selected[1], \
                core_role=value_selected[2]). \
                    with_entities(Role.role).distinct(Role.role)]

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

@app.route('/core_role/<discipline_selected>')
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

@app.route('/role/<discipline_selected>/<core_role_selected>')
# used to load the role based on the core_role selected
def role_load(discipline_selected,core_role_selected):

    role = Role.query.filter_by(discipline=discipline_selected, core_role=core_role_selected). \
                with_entities(Role.role).distinct(Role.role)
    role_array = []
    [role_array.append({'id': rol.role, 'name': rol.role}) for rol in role]

    return jsonify({'role': role_array})

@app.route('/tool_AD/<tool>/<country>')
# used to extract the AD for the tool based on the country
def tool_AD_for_country(tool,country):

    tool_ad = Tool_AD.query.filter_by(tool_name=tool, country_code=country). \
                with_entities(Tool_AD.ad_group)

    tool_ad_array = []
    [tool_ad_array.append({'ad_group': ad.ad_group}) for ad in tool_ad]

    print(jsonify({'ad_group': tool_ad_array}))
    return jsonify({'ad_group': tool_ad_array})

# record the table of users
@app.route('/user_table', methods = ['GET','POST'])
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

@app.route('/tables/<table_name>', methods = ['GET'])
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


@app.route('/login', methods=['GET', 'POST'])
# @login.user_loader
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    login_form = LoginForm()
    print(login_form.errors)
    if login_form.validate_on_submit():
        email = User.query.filter_by(email=login_form.email.data).first()
        if email is None or not email.check_password(login_form.password.data):
            # flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(email, remember=login_form.remember_me.data)
        return redirect(url_for('login_confirm'))
    return render_template('login.html', title='Sign In', login_form=login_form)

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login_confirm'))
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        user = User(user_name=registration_form.user_name.data, email=registration_form.email.data)
        user.set_password(registration_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Congratulations { registration_form.user_name.data }, you are now a registered user!','success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='SignUp', registration_form=registration_form)

@app.route('/login_confirm')
def login_confirm():
    return render_template('login_confirm.html', title='login_confirm')

@app.route("/logout")
def logout():
    logout_user()
    return render_template('logout.html')
    # return redirect(url_for('home'))


def Json_users_data_reduced(Json_data_list):
    Json_reduced = []

    [Json_reduced.append({'id' : 'id', 'user_id': Json_data['user_id'], 'role': Json_data['role'], 'country': Json_data['country']}) for Json_data in Json_data_list]

    return Json_reduced
