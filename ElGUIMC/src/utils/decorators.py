from functools import wraps
from flask import request, redirect, url_for
from src.role.RoleModule import RoleModule
from src.user.UserModule import UserModule

DES_KEY = b"eguimc19"
user_module = UserModule()
role_module = RoleModule()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        role_id = user_module.get_user_role()
        if not role_id:
            return redirect(url_for('auth_user'))
        has_permission = role_module.check_permission(role_id)
        if not has_permission:
            return redirect(url_for('auth_user'))
        return f(*args, **kwargs)
    return decorated_function
