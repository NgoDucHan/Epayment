from app import app, login, dao, models
from flask_login import login_user, logout_user, login_required
from flask import render_template, request, redirect, url_for, jsonify
from flask_paginate import Pagination, get_page_args
from app.models import *
from app.admin import *
import json
import hashlib


@login.user_loader
def user_load(user_id):
    return dao.load(user_id)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/ex")
def example():
    return render_template("example.html")


if __name__ == '__main__':
    app.run(debug=True)