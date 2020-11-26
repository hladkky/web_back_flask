from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(1000))


class UsersExercises(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('idU', 'idE'),
    )

    idU = db.Column(db.Integer, db.ForeignKey('user.id'))
    idE = db.Column(db.Integer, db.ForeignKey('exercise.id'))
