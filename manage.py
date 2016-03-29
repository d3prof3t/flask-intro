# manage.py

# Core Python Imports
import os
import urllib

# Flask Specific Imports
from flask import url_for

# Third Party Imports
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# App Specific Imports
from flasktaskr import app, db

# Pulls the in app config
app.config.from_object(os.environ['APP_SETTINGS'])

# create a migrate object
migrate = Migrate(app, db)

# create a manager object
manager = Manager(app)

# Specify the migrate command
manager.add_command('db', MigrateCommand)


# List all routes
@manager.command
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)
    
    for line in sorted(output):
        print(line)


if __name__ == '__main__':
    manager.run()
