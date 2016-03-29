# models.py


# Core Python Imports
import datetime

# App Specific Imports
from flasktaskr import db


class Task(db.Model):
    """
    DocString
    """

    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_added = db.Column(db.DateTime, default=datetime.datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, name, due_date, priority, status, user_id, date_added, date_modified):
        self.name = name
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.user_id = user_id
        self.date_added = date_added
        self.date_modified = date_modified

    def __repr__(self):
        return '<name: {}>'.format(self.name)


class User(db.Model):
    """
    DocString
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    tasks = db.relationship('Task', backref='poster')
    date_added = db.Column(db.DateTime, default=datetime.datetime.now())
    date_modified = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<username: {}>'.format(self.name)
