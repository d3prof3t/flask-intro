# tasks/views.py

###############
### Imports ###
###############

# Core Python Imports
import datetime
from functools import wraps

# Flask Imports
from flask import Blueprint

# Flask Third party imports
from flask_restful import Resource, Api, reqparse, fields, marshal

# App Specific Imports
from flasktaskr import db
# from .forms import AddTaskForm
from flasktaskr.models import Task


#########################
### Blueprints config ###
#########################

tasks_blueprint = Blueprint('tasks', __name__)
tasks = Api(tasks_blueprint)


# Fields to be serialized
resource_fields = {
    'name': fields.String,
    'due_date': fields.String,
    'priority': fields.Integer,
    'status': fields.Integer,
    'user_id': fields.Integer,
    'date_added': fields.DateTime,
    'date_modified': fields.DateTime
}


class AllTasks(Resource):
    """
    Returns all tasks
    """

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
                'data': marshal(tasks, resource_fields)
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
            # get a single task
            task = Task.query.get(task_id)
            
            if not task:
                return {
                    'success': 'false',
                    'message': 'Task does not exists for task id => {}'. \
                            format(task_id)
                }

            else:
                return {
                    'success': 'true',
                    'data': marshal(task, resource_fields)
                }


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

        try:
            
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

            return {
                'success': 'true',
                'message': 'New task inserted.',
                'data': marshal(task, resource_fields)
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
        parser.add_argument('task_id', required=True, type=int, \
                location='form', help="Task ID is required")

        # create the args object
        args = parser.parse_args(strict=True)

        try:

            # get the appropriate task
            task = db.session.query(Task).filter_by(task_id=args['task_id']). \
                    first()
        
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
        parser.add_argument('task_id', required=True, type=int, \
                location='form', help="Task ID is required")

        # create the args object
        args = parser.parse_args(strict=True)

        try:

            # get the appropriate task
            task = db.session.query(Task).filter_by(task_id=args['task_id']). \
                    first()
        
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
tasks.add_resource(AllTasks, '/tasks/<int:status_id>')
tasks.add_resource(Tasks, '/task', '/task/<int:task_id>')
