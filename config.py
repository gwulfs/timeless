import os
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = 'dat_data.db'
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'i7waonvewRRi6U'
DATABASE_PATH = os.path.join(basedir, DATABASE)