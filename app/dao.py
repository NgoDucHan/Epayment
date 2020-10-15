from app import app, login, db
import hashlib
from flask_login import login_user
from flask_admin import Admin
from app.models import *


def validate_user(username, password):
    user = User.query.filter(User.username == username,
                             User.password == password).first()
    return user


def load(user_id):
    return User.query.get(user_id)
