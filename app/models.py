import enum
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Enum, Time, Date
from datetime import datetime
from app import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship


class AccountType(enum.Enum):
    ADMIN = 1
    USER = 2
    BUSINESS = 3


class Gender(enum.Enum):
    MALE = 1
    FEMALE = 2
    UNKNOWN = 3


class ActivityType(enum.Enum):
    WITHDRAW = 1
    DEPOSIT = 2
    TRANSFER = 3

    OPEN_WALLET = 4
    DISABLE_WALLET = 5
    UPDATE_WALLET = 6

    CREATE_ACC = 7
    DISABLE_ACC = 8
    UPDATE_ACC = 9


class TransactionType(enum.Enum):
    WITHDRAW = ActivityType.WITHDRAW
    DEPOSIT = ActivityType.DEPOSIT
    TRANSFER = ActivityType.TRANSFER


# ======================= ACCOUNT ======================= #
class Account(db.Model, UserMixin):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    account_type = Column(Enum(AccountType), default=AccountType.USER)
    create_date = Column(DateTime, default=datetime.now())

    detail_account = relationship("DetailAccount", backref='account', lazy=True)
    transaction_slip = relationship("TransactionSlip", backref='account', lazy=True)
    activity_log = relationship("ActivityLog", backref='account', lazy=True)
    wallet = relationship("Wallet", backref='account', lazy=True)

    def __str__(self):
        return self.name
# ===================== END_USER ===================== #


class DetailAccount(db.Model):
    __tablename__ = "detail_account"

    id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    birthday = Column(DateTime)
    email = Column(String(50))
    address = Column(String(50))
    gender = Column(Enum(Gender), default=Gender.UNKNOWN)
    phone_number = Column(String(14))

    def __str__(self):
        return str(self.id)


class ActivityLog(db.Model):
    __tablename__ = "activity_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime_log = Column(DateTime, default=datetime.now())
    activity_log = Column(Enum(ActivityType))
    account_id = Column(Integer, ForeignKey(Account.id))

    def __str__(self):
        return str(self.id)


class Wallet(db.Model):
    __tablename__ = "wallet"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey(Account.id))
    balance_amount = Column(Float)
    active = Column(Boolean, default=True)
    bank_id = Column(String(50))
    create_date = Column(DateTime, default=datetime.now())

    transaction_slip = relationship("TransactionSlip", backref="wallet", lazy=True)

    def __str__(self):
        return str(self.id)


class TransactionSlip(db.Model):
    __tablename__ = "transaction_slip"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey(Account.id))
    wallet_id = Column(Integer, ForeignKey(Wallet.id))
    transaction_type = Column(Enum(TransactionType))
    amount = Column(Float, default=0)
    create_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return str(self.id)


if __name__ == "__main__":
    db.create_all()
