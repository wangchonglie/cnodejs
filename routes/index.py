import os
from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    send_from_directory,
)
from utils import log
from models.user import User
from config import accept_user_file_type, user_file_director
from werkzeug.utils import secure_filename
from routes import *


def current_user():
    # 从session 中找到user_id 字段，找不到就 -1
    # 然后 User.find_by 来用id 找用户
    # 找不到就返回None
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u

main = Blueprint('index', __name__)


@main.route("/register")
def register():
    return render_template("user/register.html")


@main.route("/login")
def login():
    return render_template("user/login.html")


@main.route("/to_register", methods=["GET","POST"])
def to_register():
    form = request.form
    u = User.register(form)
    return redirect(url_for('.login'))


@main.route("/profile")
def profile():
    profile_id = int(request.args.get('profile_id', -1))
    print('profile_id', profile_id)
    u = User.find_by(id=profile_id)
    now_user = current_user()
    return render_template("user/profile.html", user=u, current_user=now_user)


@main.route("/to_login", methods=["POST"])
def to_login():
    form = request.form
    # log("登录里面的form有什么：", form)
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.register'))
    else:
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index'))


def allow_file(filename):
    suffix = filename.split('.')[-1]
    return suffix in accept_user_file_type


@main.route('/addimg', methods=["POST"])
def add_img():
    u = current_user()
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if allow_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_file_director, filename))
        u.user_image = filename
        u.save()

    return redirect(url_for(".profile", profile_id=u.id))


@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(user_file_director, filename)
