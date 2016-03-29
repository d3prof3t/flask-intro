# users/views.py

###############
### Imports ###
###############

# Core Python Imports
import datetime
from functools import wraps

# Flask Imports
from flask import flash, redirect, url_for, session, request, \
        render_template, Blueprint

# Flask Third party Imports
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource, Api

# App Specific Imports
from flasktaskr import db
from .forms import RegisterForm, LoginForm
from flasktaskr.models import User


##############
### config ###
##############

users_blueprint = Blueprint('users', __name__)
users = Api(users_blueprint)


# Helper Functions


def login_required(some_func):
    @wraps(some_func)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return some_func(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap


# Routes


@users_blueprint.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('GoodBye!')
    return redirect(url_for('users.login'))


@users_blueprint.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.session.query(User).filter_by(name=form.name.data).first()
            if user is not None and user.password == form.password.data:
                session['logged_in'] = True
                session['user_id'] = user.id
                flash('Welcome')
                return redirect(url_for('tasks.tasks'))
            else:
                error = "Invalid Credentials. Please try again."
        else:
            error = "Both Fields are necessary."
    return render_template('login.html', form=form, error=error)


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    # Pass the form data to the Register Form
    form = RegisterForm(request.form)
    # Check for HTTP Method
    if request.method == 'POST':
        if form.validate_on_submit():
            # Create the Python Object to be inserted
            new_user = User (
                form.name.data,
                form.email.data,
                form.password.data
            )
            try:
                # Add the object
                db.session.add(new_user)
                # Commit the changes
                db.session.commit()
                # Redirect to /login with appropriate messages
                flash('Thanks for registering. Please Login')
                return redirect(url_for('users.login'))
            except IntegrityError:
                error = "Username or Email already exists."
                return render_template('register.html', error=error, form=form)
    return render_template('register.html', form=form, error=error)
