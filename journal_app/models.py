from .extensions import db

from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField, IntegerField,
                     BooleanField, DateTimeField, validators)


class RegisterForm(FlaskForm):
    name = StringField('', [
        validators.Length(min=1, max=100),
        validators.InputRequired()
        ])
    email = StringField('', [
        validators.Length(min=7, max=120),
        validators.Email(),
        validators.InputRequired()
        ])
    password = PasswordField('', [
        validators.Length(min=8, max=80),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match.')
        ])
    confirm = PasswordField('')


class LoginForm(FlaskForm):
    email = StringField('', [
        validators.Length(min=4, max=70),
        validators.Email(),
        validators.InputRequired()
        ])
    password = PasswordField('', [
        validators.Length(min=8, max=80),
        validators.InputRequired()
        ])
    remember = BooleanField('Remember Me?')


class EntryForm(FlaskForm):
    title = StringField('', [
        validators.Length(min=1, max=300),
        validators.InputRequired()
        ])
    content = TextAreaField('', [
        validators.Length(min=1),
        validators.InputRequired()
        ])
    word_count = IntegerField('')
    date_submitted = DateTimeField('')


class ContactForm(FlaskForm):
    name = StringField('', [
        validators.Length(min=1, max=100),
        validators.InputRequired()
        ])
    email = StringField('', [
        validators.Length(min=7, max=120),
        validators.Email(),
        validators.InputRequired()
        ])
    subject = StringField('', [
        validators.Length(min=1, max=300),
        validators.InputRequired()
    ])
    body = TextAreaField('', [
        validators.Length(min=1),
        validators.InputRequired()
    ])


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column('users_id', db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    entries = db.relationship('Entry', backref='user', lazy='dynamic')

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name


class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer,
                          db.ForeignKey('users.users_id'),
                          nullable=False)
    word_count = db.Column(db.Integer)
    date_submitted = db.Column(db.DateTime)

    def __init__(self, title, content, word_count, date_submitted):
        self.title = title
        self.content = content
        self.word_count = word_count
        self.date_submitted = date_submitted

    def __repr__(self):
        return '<Entry %r}' % self.id
