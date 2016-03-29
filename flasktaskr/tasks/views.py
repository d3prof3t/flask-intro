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
from .forms import AddTaskForm
from flasktaskr.models import Task


##############
### config ###
##############

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
        # adding get args
        parser.add_argument('status_id', required=True, action='append', \
                type=int, location='args', help='Specify type of tasks')
        args = parser.parse_args(strict=True)

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


    @marshal_with(resource_fields)
    def post(self):
        # Handling Request Params
        parser = reqparse.RequestParser()
        # adding post payload
        parser.add_argument('name', required=True, location='form')
        parser.add_argument('due_date', required=True, location='form')
        parser.add_argument('priority', required=True, type=int, \
                location='form')
        parser.add_argument('user_id', required=True, type=int, \
                location='form')
        # Creating args objecto
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
        # respond to the client
        return task


tasks.add_resource(Tasks, '/tasks', )

# Routes


# @tasks_blueprint.route('/tasks')
# @login_required
# def tasks():
#     error = None
#     form = AddTaskForm()
#     # get all completed tasks
#     closed_tasks = db.session.query(Task).filter_by(status=0).all()
#     # get all open tasks
#     open_tasks = db.session.query(Task).filter_by(status=1).all()

#     # Data Integrity Check
#     if not closed_tasks and not open_tasks:
#         error = "No tasks found."
#         return render_template('tasks.html', error=error, form=form)
#     else:
#         return render_template(
#                     'tasks.html',
#                     open_tasks=open_tasks,
#                     closed_tasks = closed_tasks,
#                     form=form
#                 )


# @tasks_blueprint.route('/add', methods=['POST'])
# @login_required
# def new_task():
#     error = None

#     # Get the basic fields from the form for creating a new task
#     task_name = request.form['name']
#     due_date = request.form['due_date']
#     priority = request.form['priority']

#     # Data Integrity Check
#     if not task_name or not due_date or not priority:
#         flash("All fields are required. Please fill in all the fields.")
#         return redirect(url_for('tasks.tasks'))
#     else:
#         # Create the Python Object to be inserted
#         task = Task (
#             request.form['name'],
#             request.form['due_date'],
#             request.form['priority'],
#             1,
#             session['user_id'],
#             datetime.datetime.now(),
#             datetime.datetime.now()
#         )
#         # Add the changes to the Session
#         db.session.add(task)
#         # Commit the changes to the DB
#         db.session.commit()
#         # Redirect to /tasks with appropriate messages
#         flash("New task was successfully created.")
#         return redirect(url_for('tasks.tasks'))


# @tasks_blueprint.route('/complete/<int:task_id>')
# @login_required
# def complete(task_id):
#     # Get the appropriate task
#     task = db.session.query(Task).filter_by(task_id=task_id).first()
#     # Set the tasks status to closed
#     task.status = 0
#     # Update the date modified to current datetime
#     task.date_modified = datetime.datetime.now()
#     # Add the changes to the Session
#     db.session.add(task)
#     # Commit the changes to the DB
#     db.session.commit()
#     # Redirect to /tasks with appropriate message
#     flash("The task was marked as complete.")
#     return redirect(url_for('tasks.tasks'))


# @tasks_blueprint.route('/delete/<int:task_id>')
# @login_required
# def delete(task_id):
#     # Get the appropriate task
#     task = db.session.query(Task).filter_by(task_id=task_id).first()
#     # Delete the Row from DB
#     db.session.delete(task)
#     # Commit the changes to the DB
#     db.session.commit()
#     # Redirect to Tasks with appropriate messages
#     flash("The task was successfully deleted")
#     return redirect(url_for('tasks.tasks'))
