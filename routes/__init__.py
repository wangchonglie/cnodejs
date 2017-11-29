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



# use db
#
# db.createUser ({
#     user: "test",
#     pwd: "test",
#     roles: [
#         {
#             role: "userAdmin",
#             db: "db"
#         }
#     ]
# })
#
#
# /usr/local/mongodb/bin/mongo -u test -p test --authenticationDatabase db
#
# #!/bin/bash
# #
# #chkconfig:2345 80 90
# #description:mongod
#
# start () {
#  /usr/local/mongodb/bin/mongod --config /usr/local/mongodb/mongod.conf
# }
#
# stop () {
#  /usr/local/mongodb/bin/mongod --config /usr/local/mongodb/mongod.conf --shutdown
# }
#
# case "$1" in
#  start)
# start
# ;;
#
#  stop)
# stop
# ;;
#
#  restart)
# stop
# start
# ;;
#  *)
#  echo
# $"Usage:$0{start|stop|restart}"
#  exit 1
# esac


