import os
from flask import Flask
from application.models import db
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your-secret-key'

basedir=os.path.abspath(os.path.dirname(__file__))
curr_dir=os.path.join(basedir, "database")
app=Flask(__name__,template_folder="templates")
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(curr_dir, "store.sqlite3")
app.secret_key = 'mykey'

CORS(app)
db.init_app(app)

app.app_context().push()

from application.controllers import *

if __name__=='__main__':
    app.debug=True
    app.run(host = '0.0.0.0')    