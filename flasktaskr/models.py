# models.py


# Core Python Imports
import datetime

# App Specific Imports
from flasktaskr import app, db

# Third Party Imports
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User(db.Model):
    """
    DocString
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Integer, default=0)
    tasks = db.relationship('Task', backref='poster', lazy='dynamic')
    date_added = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    date_modified = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())

    def __init__(self, name=None, email=None, password=None):
        self.name = name


    def generate_auth_token(self, expiration=14400):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})


    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        user.id = data['id']
        return user


    def __repr__(self):
        return '<id: {}>, <username: {}>'.format(self.id, self.name)


class Task(db.Model):
    """
    DocString
    """

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_added = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    date_modified = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())

    def __init__(self, name, due_date, priority, status, user_id, date_added, date_modified):
        self.name = name
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def __repr__(self):
        return '<name: {}>'.format(self.name)
