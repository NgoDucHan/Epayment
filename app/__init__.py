from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


passKiet = "kiet01685258917"
passHan = "1803"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:" + passHan + "@localhost/db_epayment"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = '\xeen\x83\xfe\xe2\xd9ZS\x02\x7f_f\xeb\xde\xa2\xd4'

db = SQLAlchemy(app=app)

admin = Admin(app=app, name="E-Payment System", template_mode="bootstrap3")

login = LoginManager(app=app)
