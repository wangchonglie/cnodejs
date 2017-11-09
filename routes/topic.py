from flask import render_template, request, redirect, url_for, Blueprint, abort
from routes import *
from utils import log

from models.topic import Topic
from models.reply import Reply

main = Blueprint('topic', __name__)


import uuid
csrf_tokens = set()


@main.route("/")
def index():
    ms = Topic.all()
    token = str(uuid.uuid4())
    csrf_tokens.add(token)
    return render_template("topic/index.html", ms=ms, token=token)


@main.route("/<int:id>")
def detail(id):
    m = Topic.get(id)
    return render_template("topic/detail.html", topic=m)


@main.route("/new")
def new():
    return render_template("topic/new.html")


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
def delete():
    delete_id = int(request.args.get('id'))
    token = request.args.get('token')
    u = current_user()
    if token in csrf_tokens:
        csrf_tokens.remove(token)
        if u is not None:
            Topic.delete(delete_id)
            for i in range(len(Reply.find_all(topic_id=delete_id))):
                Reply.delete_reply(delete_id)
            return redirect(url_for('.index'))
    else:
        abort(403)
