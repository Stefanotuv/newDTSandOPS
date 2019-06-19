__author__ = "stefanotuv"

import sys
import os.path

# export the file path to make it working on atom
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))
# TEMPLATE_DIR = os.path.abspath('../tests_templates')
STATIC_DIR = os.path.abspath('static')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','xls','xlsx'])
TABLE_LIST = ['Countries', 'Roles', 'Roles_Tools', 'Tool_AD', 'Tools', 'User']
from pathlib import Path

# UPLOAD_FOLDER = os.path.abspath('static\data_import')
# LOCAL_DB_FOLDER = os.path.abspath('../static/db_local')
# UPLOAD_INITIATE_FOLDER = os.path.abspath('static\data_import')
# UPLOAD_INITIATE_FOLDER = os.path.join(os.path.abspath(''),'static/data_import')

# UPLOAD_FOLDER = os.path.join(os.path.join(os.path.abspath(''),Path('static/data_import')))


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__),Path('data_import'))
LOCAL_DB_INITIATE_FOLDER = os.path.join(os.path.dirname(__file__),Path('db_local'))
UPLOAD_INITIATE_FOLDER = os.path.join(os.path.dirname(__file__),Path('data_import'))
UPLOAD_INITIATE_FOLDER = os.path.join(os.path.dirname(__file__),Path('data_import'))


DATABASE_FILE_CONNECTIONS = 'db_connection.json'

# LOCAL_DB_INITIATE_FOLDER = os.path.abspath('db_local')
# DATA_IMPORT_DIR = '../../static/data_import'
SERVER_URI = ""
DBTYPE = 'mongo' # default value mysql
# assign in the app to connect the different type of DB
# it has to include the user and password format: 'postgresql://usr:pass@localhost:5432/sqlalchemy'
