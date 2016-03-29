# users/forms.py

# Flask third party imports
from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, SelectField, \
        PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class RegisterForm(Form):
    """
    DocString
    """

    name = StringField('Username',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = StringField('Email',
        validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField('Password',
        validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField('Confirm Password',
        validators=[DataRequired(),
        EqualTo('password', message="Passwords must match")]
    )


class LoginForm(Form):
    """
    DocString
    """

    name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
