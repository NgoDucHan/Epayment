from app import app, login, db
import hashlib
from flask_login import login_user
from flask_admin import Admin
from app.models import *


def validate_account(username, password):
    account = Account.query.filter(Account.username == username,
                                   Account.password == password).first()
    return account


def load(account_id):
    return Account.query.get(account_id)
