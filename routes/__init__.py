from flask import session, abort
from models.user import User
from functools import wraps
from utils import log


def current_user():
    uid = session.get('user_id', '')
    u = User.find_by(id=uid)
    return u


def login_permission(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        u = current_user()
        if u is None:
            abort(403)
        else:
            return f(*args, **kwargs)
    return decorator


def admin_permission(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        u = current_user()
        if u is None:
            abort(403)
        elif u.role == 0:
            return f(*args, **kwargs)
        else:
            abort(403)
    return decorator



