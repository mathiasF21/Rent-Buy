from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired,EqualTo, Regexp, Length

class User(UserMixin):
    def __init__(self, email, password, name):
        if not isinstance(email, str):
            raise TypeError('Email must be a string')
        if not isinstance(password, str):
            raise TypeError('Password must be a string')
        if not isinstance(name, str):
            raise TypeError('Name must be a string')
        self.email = email
        self.name= name
        self.password = password
        self.id = None
        self.member_type = None
        self.funds = None
        
    def __repr__(self):
        return f'User({self.name}, {self.email})'
        
    def __str__(self):
        value = f'{self.name}: {self.email}'
        return value

class SignupForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    name = StringField("Name", validators=[DataRequired(), Regexp("[A-Za-z]", message="Name must contain only letters"), Length(min=1)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ProfileEdit(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    funds = IntegerField("Add funds:", validators=[DataRequired()])
    submit = SubmitField('Update')

class ChangePassword(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Update')

