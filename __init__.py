import os
import sys

from flask import Flask
# sqlite database package
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

# db env settings(sqlite)
WINDOWS = sys.platform.startswith('win')
if WINDOWS:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# db settings(path, SQLAlchemy)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = '請先登入'


@login_manager.user_loader
def load_user(user_id):
    from todo_list.models import User
    user = User.query.get(int(user_id))
    return user


# place context in every templates
# @app.context_processor
# def place_user_in_templates():
#     from todo_list.models import User
#     user = User.query.first()
#     return dict(user=user)

# avoid inherit loop (A->B and B->A)
from todo_list import views, errors, commands
