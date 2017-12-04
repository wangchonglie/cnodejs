import os
from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    send_from_directory,
)
from flask import jsonify
from config import accept_user_file_type, user_file_director
from werkzeug.utils import secure_filename
from routes import *


main = Blueprint('index', __name__)


@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user() is not None:
        session.pop('user_id')
    return render_template("user/register.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    return render_template("user/login.html")


@main.route("/to_register", methods=["POST"])
def to_register():
    data_ajax = request.get_json()
    u = User.register(data_ajax['username'], data_ajax['signature'], data_ajax['password'])
    if u['msg'] == '注册成功！':
        data = {
            "result": True,
            "msg": "请登录。"
        }
        return jsonify(data)
    elif u['msg'] == '该用户名已经被注册！':
        data = {
            "result": False,
            "msg": "该用户名已经被注册！"
        }
        return jsonify(data)
    else:
        data = {
            "result": False,
            "msg": "用户名和密码应4位或以上！"
        }
        return jsonify(data)


@main.route("/profile")
def profile():
    profile_id = int(request.args.get('profile_id', -1))
    u = User.find_by(id=profile_id)
    now_user = current_user()
    return render_template("user/profile.html", user=u, current_user=now_user)


@main.route("/to_login", methods=["POST"])
def to_login():
    data_ajax = request.get_json()
    u = User()
    u.username = data_ajax['username']
    u.password = data_ajax['password']
    user = User.find_by(username=u.username)
    if user is not None and user.password == u.salted_password(u.password):
        session['user_id'] = user.id
        session.permanent = True
        data = {
            "result": True,
            "user_id": user.id
        }
        return jsonify(data)
    else:
        data = {"result":False,"user_id":None}
        return jsonify(data)


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

    return redirect(url_for(".new_profile", profile_id=u.id))


@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(user_file_director, filename)


@main.route("/profile_edit", methods=["POST"])
@login_permission
def profile_edit():
    u = current_user()
    data_ajax = request.get_json()
    if data_ajax['username'] != '' or data_ajax['signature'] != '':
        if data_ajax['username'] != '':
            u.username = data_ajax['username']
        if data_ajax['signature'] != '':
            u.signature = data_ajax['signature']
        u.save()
        data = {
            "result": True,
            "msg": "修改成功。",
        }
        return jsonify(data)
    else:
        data = {
            "result": True,
            "msg": "您未修改任何内容，请确认。",
        }
        return jsonify(data)


@main.route("/new_profile")
@login_permission
def new_profile():
    u = current_user()
    return render_template("user/profile_edit.html", user=u)


@main.route("/password_edit", methods=["POST"])
@login_permission
def password_edit():
    u = current_user()
    data_ajax = request.get_json()
    print(data_ajax)
    if data_ajax['old_password'] != '' and data_ajax['new_password'] != '':
        if u.password == u.salted_password(data_ajax['old_password']):
            if len(data_ajax['new_password']) > 4:
                u.password = u.salted_password(data_ajax['new_password'])
                u.save()
                session.pop('user_id')
                data = {
                    "result": True,
                    "msg": "修改成功。",
                }
                return jsonify(data)
            else:
                data = {
                    "result": False,
                    "msg": "新密码要4位以上。",
                }
                return jsonify(data)
        else:
            data = {
                "result": False,
                "msg": "当前密码错误，请确认。",
            }
            return jsonify(data)
    else:
        data = {
            "result": False,
            "msg": "当前密码或新密码未输入，请确认。",
        }
        return jsonify(data)
