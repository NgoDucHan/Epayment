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


@app.route("/login", methods=['get', 'post'])
def login():
    errmsg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        account = dao.validate_account(username.strip(), password)
        if account and account.account_type == AccountType.ADMIN:
            login_user(user=account)
            return redirect("/admin")
        else:
            if account and (account.account_type == AccountType.USER or account.account_type == AccountType.BUSINESS):
                login_user(user=account)
                return redirect("/")
            else:
                errmsg = "Username or password is incorrect!"
                return render_template("login.html", errmsg=errmsg)
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/ex")
def example():
    return render_template("example.html")


@app.context_processor
def common_data():
    return {
        'gender': Gender,
        'account_type': AccountType,
        'activity_type': ActivityType,
        'transaction_type': TransactionType
    }


if __name__ == '__main__':
    app.run(debug=True)
