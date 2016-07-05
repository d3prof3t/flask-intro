# users/views.py

###############
### Imports ###
###############

# Core Python Imports
import datetime, time, codecs, base64
from functools import wraps

# Flask Imports
from flask import Blueprint, request

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


# user data to be serailized

user_post_resource_fields = {
    'name': fields.String
}

# Resources

class Users(Resource):
    """
    Resource for Users
    """

    def post(self):
        
        # instantiate the reqparse object
        parser = reqparse.RequestParser()

        # payload data sanity check
        parser.add_argument('name', location='form', required=True, \
                help='Name is a required field.')
        parser.add_argument('email', required=True, \
                location='form', help='Email is required field.')
        parser.add_argument('password', required=True, \
                location='form', help='Password is a required field.')

        # create the args object
        args = parser.parse_args(strict=True)
        
        # create the user object to be inserted
        user = User(
            args['name'],
            args['email'],
            bcrypt.generate_password_hash(args['password'])
        )

        # check if user is already registered
        user_exists = User.query.filter_by(email=args['email']).first()
        if not user_exists:
            try:
                # add the object
                db.session.add(user)

                # commit the changes
                db.session.commit()

                return {
                    'success': 'true',
                    'data': marshal(user, user_post_resource_fields)
                }, 201

            except IntegrityError:
                return {
                    'success': 'false',
                    'message': 'User already exists.'
                }
        else:
            return {
                'success': 'false',
                'message': 'User already exists.'
            }


class Token(Resource):
    """
    Generates Auth Token for users
    """

    def post(self):

        # get the user from db
        user = User.query.filter_by(email=request.authorization.username).first()
        if not user:
            return {
                    'success': 'false',
                    'message': 'User not found.'
            }
        else:
            if user.password.startswith(r'\x'):
                user.password = codecs.decode(bytes(user.password[2:], \
                            'ascii'), 'hex')
            # verify password
            if bcrypt.check_password_hash(user.password, \
                    request.authorization.password):
                # generate auth token
                auth_token = user.generate_auth_token()
                return {
                    'token': auth_token.decode('ascii')
                }


# Bind the resources to routes
users.add_resource(Users, '/api/v1/user')
users.add_resource(Token, '/api/v1/token')
