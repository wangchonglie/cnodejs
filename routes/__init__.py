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
            log('未登录')
            abort(403)
        else:
            return f(*args, **kwargs)
    return decorator


def admin_permission(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        u = current_user()
        if u is None:
            log('未登录')
            abort(403)
        elif u.role == 11:
            log('管理员')
            return f(*args, **kwargs)
        else:
            log('非管理员')
            abort(403)
    return decorator



