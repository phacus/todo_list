from todo_list import db
from flask_login import UserMixin
# password security
from werkzeug.security import generate_password_hash, check_password_hash

import datetime


# models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    tasks = db.relationship('Task', backref='user')

    # create password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # valid password using hash
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(20))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
