# tasks/views.py

###############
### Imports ###
###############

# Core Python Imports
import datetime
from functools import wraps

# Flask Imports
from flask import flash, redirect, url_for, session, request, \
        render_template, Blueprint

# Flask Third party imports
from flask_restful import Resource, Api, reqparse, fields, marshal_with

# App Specific Imports
from flasktaskr import db
# from .forms import AddTaskForm
from flasktaskr.models import Task


#########################
### Blueprints config ###
#########################

tasks_blueprint = Blueprint('tasks', __name__)
tasks = Api(tasks_blueprint)

# Helper Functions


# def login_required(some_func):
#     @wraps(some_func)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return some_func(*args, **kwargs)
#         else:
#             flash('You need to login first.')
#             return redirect(url_for('users.login'))
#     return wrap

# Fields to be serialized
resource_fields = {
    'task_id': fields.Integer,
    'name': fields.String,
    'due_date': fields.String,
    'priority': fields.Integer,
    'status': fields.Integer,
    'user_id': fields.Integer,
    'date_added': fields.DateTime,
    'date_modified': fields.DateTime
}

class Tasks(Resource):

    @marshal_with(resource_fields)
    def get(self):
        # Handling Request Params
        parser = reqparse.RequestParser()

        parser.add_argument('status_id', required=True, action='append', \
                type=int, location='args', help='Specify type of tasks')
        args = parser.parse_args()

        if 1 in args['status_id']:
            # get open tasks
            open_tasks = db.session.query(Task).filter_by(status=1).all()
        else:
            open_tasks = []

        if 0 in args['status_id']:
            # get closed tasks
            closed_tasks = db.session.query(Task).filter_by(status=0).all()
        else:
            closed_tasks = []

        # prepare response
        if not open_tasks and not closed_tasks:
            return {'success': 'false', 'message': 'No tasks found'}
        elif open_tasks and not closed_tasks:
            return open_tasks
        elif not open_tasks and closed_tasks:
            return closed_tasks
        else:
            all_tasks = []
            all_tasks.append(open_tasks)
            all_tasks.append(closed_tasks)
            return all_tasks


    @marshal_with(resource_fields)
    def post(self):
        
        # instantiate reqparse object
        parser = reqparse.RequestParser()
        
        # payload data sanity check
        parser.add_argument('name', required=True, location='form')
        parser.add_argument('due_date', required=True, location='form')
        parser.add_argument('priority', required=True, type=int, \
                location='form')
        parser.add_argument('user_id', required=True, type=int, \
                location='form')

        # creating args object
        args = parser.parse_args(strict=True)
        
        # create new task object to be inserted
        task = Task(
            args['name'],
            args['due_date'],
            int(args['priority']),
            1,
            args['user_id'],
            datetime.datetime.now(),
            datetime.datetime.now()
        )

        # insert the new task
        db.session.add(task)

        # commit the changes
        db.session.commit()

        return task


    @marshal_with(resource_fields)
    def put(self):

        # instantiate reqparse object
        parser = reqparse.RequestParser()

        # payload data sanity check
        parser.add_argument('task_id', required=True, type=int, \
                location='form', help="Task ID is required")

        # create the args object
        args = parser.parse_args(strict=True)

        # get the appropriate task
        task = db.session.query(Task).filter_by(task_id=args['task_id']). \
                first()
        
        # set the task staus as closed
        task.status = 0

        # update date modified
        task.date_modified = datetime.datetime.now()
        
        # add the changes to the session
        db.session.add(task)

        # commit the changes to the db
        db.session.commit()

        return task


    @marshal_with(resource_fields)
    def delete(self):

        # instantiate the reqparse object
        parser = reqparse.RequestParser()

        # payload data sanity check
        parser.add_argument('task_id', required=True, type=int, \
                location='form', help="Task ID is required")

        # create the args object
        args = parser.parse_args(strict=True)

        # get the appropriate task
        task = db.session.query(Task).filter_by(task_id=args['task_id']). \
                first()
        
        # delete the row from db
        db.session.delete(task)

        # commit the changes to the db
        db.session.commit()

        return task


# bind the resource to a route
tasks.add_resource(Tasks, '/tasks', )
