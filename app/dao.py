from app import app, login, db
import hashlib
from flask_login import login_user, current_user
from flask_admin import Admin
from app.models import *


def _validate_user(_username, _password):
    account = Account.query.filter(Account.username == _username,
                                   Account.password == _password).first()
    return account


def load(account_id):
    return Account.query.get(account_id)


def load_newest_id():
    account = Account.query.order_by(Account.id.desc()).first()
    return account


def add_new_account(name, username, password):
    try:
        account = Account()
        account.name = name
        account.username = username
        account.password = password

        db.session.add(account)
        db.session.commit()
        return account
    except Exception as ex:
        print(ex)
        return False


def search_account_by_name(kw_name):
    kw_name = str(kw_name).strip()
    acc = Account.query.filter(Account.name.contains(kw_name))
    return acc.all()


def get_account_by_id(account_id):
    return Account.query.filter(Account.id == account_id).first()


def load_wallet(account_id):
    return Wallet.query.filter(Wallet.account_id == account_id).first()


def add_new_wallet(account):
    try:
        wallet = Wallet()
        wallet.balance_amount = 0
        wallet.account_id = account.id

        db.session.add(wallet)
        db.session.commit()
        activity_log(ActivityType.OPEN_WALLET, account.id)
        return True
    except Exception as ex:
        print(ex)
        return False


def update_wallet_amount(wallet_id, amount, bank_id=None):
    try:
        wallet = Wallet.query.filter(Wallet.id == wallet_id).first()
        balance = wallet.balance_amount
        new_balance = balance + float(amount)
        wallet.balance_amount = new_balance

        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


def transaction(account_id, wallet_id, transaction_type, amount, another_account_id=None):
    try:
        if transaction_type:
            amount = float(amount)
            if transaction_type == TransactionType.WITHDRAW:
                withdraw = TransactionSlip()
                withdraw.account_id = account_id
                withdraw.wallet_id = wallet_id

                withdraw.amount = amount
                withdraw.transaction_type = transaction_type

                db.session.add(withdraw)
                db.session.commit()
                activity_log(ActivityType.WITHDRAW, account_id)
                update_wallet_amount(wallet_id, amount)
                return True
            elif transaction_type == TransactionType.DEPOSIT:
                if check_amount(wallet_id, amount):
                    deposit = TransactionSlip()
                    deposit.account_id = account_id
                    deposit.wallet_id = wallet_id

                    deposit.amount = -amount
                    deposit.transaction_type = transaction_type

                    db.session.add(deposit)
                    db.session.commit()
                    activity_log(ActivityType.DEPOSIT, account_id)
                    update_wallet_amount(wallet_id, -amount)
                    return True
                return False
            elif transaction_type == TransactionType.TRANSFER:
                if check_amount(wallet_id, amount):
                    transfer = TransactionSlip()
                    transfer.account_id = account_id
                    transfer.wallet_id = wallet_id

                    transfer.amount = -amount
                    transfer.transaction_type = transaction_type

                    db.session.add(transfer)
                    db.session.commit()

                    update_wallet_amount(wallet_id, -amount)

                    other_wallet = load_wallet(another_account_id)
                    update_wallet_amount(other_wallet.id, amount)

                    activity_log(ActivityType.TRANSFER, account_id)
                    return True
                return False
            return False
    except Exception as ex:
        print(ex)
        return False


def check_amount(wallet_id, amount):
    wallet = Wallet.query.filter(Wallet.id == wallet_id).first()

    if wallet.balance_amount >= amount:
        return True
    return False


def activity_log(activity_type, account_id):
    try:
        activity = ActivityLog()
        activity.account_id = account_id
        activity.activity_log = activity_type

        db.session.add(activity)
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False
