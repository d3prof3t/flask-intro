# users/views.py

###############
### Imports ###
###############

# Core Python Imports
import datetime, time
from functools import wraps

# Flask Imports
from flask import g, Blueprint

# Flask Third party Imports
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource, Api, fields, marshal, reqparse

# App Specific Imports
from flasktaskr import db, bcrypt, auth
from flasktaskr.models import User


##############
### config ###
##############

users_blueprint = Blueprint('users', __name__)
users = Api(users_blueprint)


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


# user data to be serailized
user_post_resource_fields = {
    'name': fields.String,
    'email': fields.String,
    'password': fields.String
}

class Users(Resource):
    """
    Resource for Users
    """

    def get(self):
        return "Hello World"


    def post(self):
        
        # instantiate the reqparse object
        parser = reqparse.RequestParser()

        # payload data sanity check
        parser.add_argument('name', location='form', \
                help='Name is a required field.')
        parser.add_argument('email', required=True, location='form', \
                help='Email is required field.')
        parser.add_argument('password', required=True, location='form', \
                help='Password is a required field.')

        # create the args object
        args = parser.parse_args()
        
        # check for login/register
        if not args['name']:
            # login
            user = User.query.filter_by(email=args['email']).first()
            if not user:
                return {
                    'success': 'false',
                    'message': 'User not found.'
                }
            else:
                # if bcrypt.check_password_hash(user.password, args['password']):
                #     return "match"
                # return "not match"
                # auth_token = user.generate_auth_token()
                # print(auth_token)
                # time.sleep(2)
                # verified = user.verify_auth_token(auth_token) 
                # print(verified)
                return "yea"
        else:
            # create the user object to be inserted
            new_user = User(
               args['name'],
               args['email'],
               bcrypt.generate_password_hash(args['password'])
            )

            # check if user is already registered
            user_exists = User.query.filter_by(email=args['email']).first()
            if not user_exists:
                try:
                    # add the object
                    db.session.add(new_user)

                    # commit the changes
                    db.session.commit()

                    # close the connection
                    db.session.close()

                    return {
                        'success': 'true',
                        'data': marshal(user, user_post_resource_fields)
                    }, 201
                except Exception as e:
                    return {
                        'success': 'false',
                        'message': '{}'.format(e)
                    }
            else:
                return {
                    'success': 'false',
                    'message': 'User already exists.'
                }


users.add_resource(Users, '/api/v1/users')

# Routes


# @users_blueprint.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     session.pop('user_id', None)
#     flash('GoodBye!')
#     return redirect(url_for('users.login'))
# 
# 
# @users_blueprint.route('/', methods=['GET', 'POST'])
# def login():
#     error = None
#     form = LoginForm(request.form)
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             user = db.session.query(User).filter_by(name=form.name.data).first()
#             if user is not None and user.password == form.password.data:
#                 session['logged_in'] = True
#                 session['user_id'] = user.id
#                 flash('Welcome')
#                 return redirect(url_for('tasks.tasks'))
#             else:
#                 error = "Invalid Credentials. Please try again."
#         else:
#             error = "Both Fields are necessary."
#     return render_template('login.html', form=form, error=error)
# 
# 
# @users_blueprint.route('/register', methods=['GET', 'POST'])
# def register():
#     error = None
#     # Pass the form data to the Register Form
#     form = RegisterForm(request.form)
#     # Check for HTTP Method
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             # Create the Python Object to be inserted
#             new_user = User (
#                 form.name.data,
#                 form.email.data,
#                 form.password.data
#             )
#             try:
#                 # Add the object
#                 db.session.add(new_user)
#                 # Commit the changes
#                 db.session.commit()
#                 # Redirect to /login with appropriate messages
#                 flash('Thanks for registering. Please Login')
#                 return redirect(url_for('users.login'))
#             except IntegrityError:
#                 error = "Username or Email already exists."
#                 return render_template('register.html', error=error, form=form)
#     return render_template('register.html', form=form, error=error)
