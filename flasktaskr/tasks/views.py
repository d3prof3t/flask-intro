# tasks/views.py

###############
### Imports ###
###############

# Core Python Imports
import datetime
from functools import wraps

# Flask Imports
from flask import Blueprint, request, g

# Flask Third party imports
from flask_restful import Resource, Api, reqparse, fields, marshal

# App Specific Imports
from flasktaskr import db
from flasktaskr.models import Task, User


#########################
### Blueprints config ###
#########################

tasks_blueprint = Blueprint('tasks', __name__)
tasks = Api(tasks_blueprint)


# validate token decorator
def validate_token(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        auth_token = request.headers.get('X-auth-token')
        if not auth_token:
            return {
                'success': 'false',
                'message': 'Token not found.'
            }
        else:
            user = User.verify_auth_token(auth_token)
            if not user:
                return {
                    'success': 'false',
                    'message': 'Invalid Token.'
                }
            else:
                g.user = user
                return f(*args, **kwargs)
    return wrap


# Fields to be serialized

task_resource_fields = {
    'name': fields.String,
    'due_date': fields.String,
    'priority': fields.Integer,
    'status': fields.Integer,
    'user_id': fields.Integer,
    'date_added': fields.DateTime,
    'date_modified': fields.DateTime
}

user_resource_fields = {
    'name': fields.String,
    'id': fields.Integer,
    'password': fields.String
}


# Resources

class AllTasks(Resource):
    """
    Returns all tasks
    """

    @validate_token
    def get(self, status_id):

        # get tasks based on status_id
        tasks = Task.query.filter_by(status=status_id).all()

        if not tasks:
            return {
                'success': 'false',
                'message': 'No tasks found.'
            }

        else:
            return {
                'success': 'true',
                'data': marshal(tasks, task_resource_fields)
            }


class Tasks(Resource):
    """
    Single Task Resource
    """

    def get(self, task_id):

        # check for task_id
        if not task_id:
            return {
                'success': 'false',
                'message': 'No task id specified.'
            }

        else:
            try:

                # get a single task
                task = Task.query.get_or_404(task_id)
                return {
                    'success': 'true',
                    'data': marshal(task, task_resource_fields)
                }
            except Exception as e:
                return {
                    'success': 'false',
                    'message': '{}'.format(e)
                }


    @validate_token
    def post(self):

        # instantiate reqparse object
        parser = reqparse.RequestParser()

        # payload data sanity check
        parser.add_argument('name', required=True, \
                location='form')
        parser.add_argument('due_date', required=True, \
                location='form')
        parser.add_argument('priority', required=True, type=int, \
                location='form')

        # creating args object
        args = parser.parse_args(strict=True)

        # create a new task
        try:
            # create new task object to be inserted
            task = Task(
                name=args['name'],
                due_date=args['due_date'],
                priority=int(args['priority']),
                status=1,
                user_id=User.poster,
                date_added=datetime.datetime.now(),
                date_modified=datetime.datetime.now()
            )

            # insert the new task
            db.session.add(task)

            # commit the changes
            db.session.commit()

            return {
                'success': 'true',
                'message': 'New task inserted.',
                'data': marshal(task, task_resource_fields)
            }, 201

        except Exception as e:
            return {
                'success': 'false',
                'message': '{}'.format(e)
            }

    def put(self):

        # instantiate reqparse object
        parser = reqparse.RequestParser()

        # payload data sanity check
        parser.add_argument('task_id', required=True, type=int,
                            location='form', help="Task ID is required")

        # create the args object
        args = parser.parse_args(strict=True)

        try:

            # get the appropriate task
            task = Task.query.get_or_404(args['task_id'])

            # set the task staus as closed
            task.status = 2

            # update date modified
            task.date_modified = datetime.datetime.now()

            # add the changes to the session
            db.session.add(task)

            # commit the changes to the db
            db.session.commit()

            return {
                'success': 'true',
                'message': 'Task updated successfully.',
                'data': marshal(task, resource_fields)
            }

        except Exception as e:
            return {
                'success': 'false',
                'message': '{}'.format(e)
            }

    def delete(self):

        # instantiate the reqparse object
        parser = reqparse.RequestParser()

        # payload data sanity check
        parser.add_argument('task_id', required=True, type=int,
                            location='form', help="Task ID is required")

        # create the args object
        args = parser.parse_args(strict=True)

        try:

            # get the appropriate task
            task = Task.query.get_or_404(args['task_id'])

            # delete the row from db
            db.session.delete(task)

            # commit the changes to the db
            db.session.commit()

            return {
                'success': 'true',
                'message': 'Task successfully deleted.'
            }

        except Exception as e:
            return {
                'success': 'false',
                'message': '{}'.format(e)
            }


# bind the resource to a route
tasks.add_resource(AllTasks, '/api/v1/tasks/<int:status_id>')
tasks.add_resource(Tasks, '/api/v1/task', '/api/v1/task/<int:task_id>')
