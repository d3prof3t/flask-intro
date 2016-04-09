# flasktaskr/__init__.py

# Core Python Imports
import os

# Flask related imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
bcrypt = Bcrypt(app)
auth = HTTPBasicAuth()
db = SQLAlchemy(app)

from flasktaskr.users.views import users_blueprint
from flasktaskr.tasks.views import tasks_blueprint

# register our blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)
