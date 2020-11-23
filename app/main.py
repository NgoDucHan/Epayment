from click import password_option

from app import app, login, models, dao, momo_api
from flask_login import login_user, logout_user, login_required, current_user
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
        _username = request.form.get("username")
        _password = request.form.get("password")
        _password = str(hashlib.md5(_password.strip().encode("utf-8")).hexdigest())
        account = dao._validate_user(_username.strip(), _password)

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


@app.route("/payment", methods=['get', 'post'])
@login_required
def payment_total():
    total = request.form.get("amount")
    req = None
    if total:
        req = momo_api.CreateOrderByMomo(total=total)

    return render_template("payment.html", req=req)


@app.route("/search-to-transfer")
@login_required
def search_account():
    errmsg = ""
    name = request.args.get("name")
    accounts = None
    if name:
        accounts = dao.search_account_by_name(kw_name=name)
        if not accounts:
            errmsg = "Account is not found!"
    return render_template("search_transfer.html", accounts=accounts, errmsg=errmsg)


@app.route("/transfer", methods=['get', 'post'])
@login_required
def transfer():
    errmsg = ""
    sucmsg = ""
    wallet = None
    account_id = request.args.get("account_id")
    account_name = request.args.get("account_name")
    id = request.form.get("account_id")

    # account = None
    if request.method == 'POST':
        amount = request.form.get("amount")
        frag = float(amount)

        password = request.form.get("password")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())

        account_id = request.args.get("account_id")
        account = dao.get_account_by_id(account_id=id)

        if password == current_user.password:
            if amount:
                if frag >= 1000:
                    if id:
                        wallet = dao.load_wallet(current_user.id)
                        dao.transaction(account_id=current_user.id, wallet_id=wallet.id,
                                        transaction_type=TransactionType.TRANSFER, amount=amount,
                                        another_account_id=id)
                        sucmsg = "Transfer completed!"
                    else:
                        errmsg = "Can not complete! {0} {1} {2}".format(account_id, id, account.id)
                else:
                    errmsg = "Amount must be more than 1000!"
        else:
            errmsg = "Password is incorrect!"
    return render_template("transfer.html", sucmsg=sucmsg, wallet=wallet,
                           errmsg=errmsg, account_id=account_id, account_name=account_name)


@app.route("/transaction/withdraw", methods=['get', 'post'])
@login_required
def withdraw():
    errmsg = ""
    wallet = None
    req = None
    if request.method == 'POST':
        amount = request.form.get("amount")
        frag = float(amount)
        password = request.form.get("password")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        if password == current_user.password:
            if amount:
                if frag > 0:
                    req = momo_api.CreateOrderByMomo(total=amount)
                    if req['message'] == 'Success':
                        wallet = dao.load_wallet(current_user.id)
                        dao.transaction(account_id=current_user.id, wallet_id=wallet.id,
                                        transaction_type=TransactionType.WITHDRAW, amount=amount)
                elif frag < 0:
                    errmsg = "Amount must be more than zero!"
        else:
            errmsg = "Password is incorrect!"
    return render_template("withdraw.html", req=req, wallet=wallet, errmsg=errmsg)


@app.route("/transaction/deposit", methods=['get', 'post'])
@login_required
def deposit():
    errmsg = ""
    wallet = None
    req = None
    if request.method == 'POST':
        amount = request.form.get("amount")
        frag = float(amount)
        password = request.form.get("password")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        if password == current_user.password:
            if amount:
                if frag > 0:
                    req = momo_api.CreateOrderByMomo(total=amount)
                    if req['message'] == 'Success':
                        wallet = dao.load_wallet(current_user.id)
                        dao.transaction(account_id=current_user.id, wallet_id=wallet.id,
                                        transaction_type=TransactionType.DEPOSIT, amount=amount)
                elif frag < 0:
                    errmsg = "Amount must be more than zero!"
        else:
            errmsg = "Password is incorrect!"
    return render_template("deposit.html", req=req, wallet=wallet, errmsg=errmsg)


@app.route("/register",  methods=['get', 'post'])
def register():
    errmsg = ""
    sucmsg = ""
    if not current_user.is_authenticated:
        if request.method == 'POST':
            name = request.form.get("name")
            username = request.form.get("username")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            if not password == confirm_password:
                errmsg = "Password is not correct!"
            else:
                password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
                try:
                    add_account_result = dao.add_new_account(name, username, password)
                    if add_account_result:
                        add_wallet_result = dao.add_new_wallet(dao.load_newest_id())
                    if add_wallet_result:
                        sucmsg = "Created successful!"
                except Exception as ex:
                    print(ex)
                    errmsg = "Can not create!"
    else:
        errmsg = "You need log out use this!"
    return render_template("register.html", sucmsg=sucmsg, errmsg=errmsg)


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
