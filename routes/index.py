from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
)
from utils import log
from models.user import User


def current_user():
    # 从session 中找到user_id 字段，找不到就 -1
    # 然后 User.find_by 来用id 找用户
    # 找不到就返回None
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u

main = Blueprint('index', __name__)


@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/register", methods=["POST"])
def register():
    form = request.form
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=["POST"])
def login():
    form = request.form
    # log("登录里面的form有什么：", form)
    u = User.validate_login(form)
    if u is None:
        log('登录失败')
        return redirect(url_for('.index'))
    else:
        log('登录成功')
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('topic.index'))
