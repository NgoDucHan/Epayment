from app import admin, db
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import current_user, logout_user
from flask import redirect
from app.models import *


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def is_visible(self):
        if current_user.account_type == AccountType.ADMIN:
            return True
        return False


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AccountView(ModelView):
    column_display_pk = True
    can_create = True
    can_delete = True
    can_set_page_size = True
    can_export = True


class DetailAccountView(ModelView):
    column_display_pk = True
    can_create = False
    can_delete = False
    can_set_page_size = True
    can_export = True


class WalletView(ModelView):
    column_display_pk = True
    can_create = False
    can_delete = False
    can_set_page_size = True
    can_export = True


class ActivityLogView(ModelView):
    column_display_pk = True
    can_create = False
    can_delete = False
    can_set_page_size = True
    can_export = True


class TransactionSlipView(ModelView):
    column_display_pk = True
    can_create = False
    can_delete = False
    can_set_page_size = True
    can_export = True


class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login')


admin.add_view(AccountView(Account, db.session))
admin.add_view(DetailAccountView(DetailAccount, db.session))
admin.add_view(WalletView(Wallet, db.session))
admin.add_view(ActivityLogView(ActivityLog, db.session))
admin.add_view(TransactionSlipView(TransactionSlip, db.session))
admin.add_view(LogoutView(name="Logout"))
