from flask import render_template, request, redirect, url_for, Blueprint, abort
from routes import *
from utils import log

from models.topic import Topic
from models.reply import Reply
from models.board import Board

main = Blueprint('topic', __name__)


import uuid
csrf_tokens = set()


@main.route("/")
def index():
    token = str(uuid.uuid4())
    csrf_tokens.add(token)
    board_id = int(request.args.get("board_id", 0))
    print(board_id)
    if board_id == 0:
        ms = Topic.all()
    else:
        ms = Topic.find_all(board_id=board_id)
    bs = Board.all()
    return render_template("topic/index.html", ms=ms, token=token, bs=bs)


@main.route("/<int:id>")
def detail(id):
    m = Topic.get(id)
    return render_template("topic/detail.html", topic=m)


@main.route("/new")
def new():
    bs = Board.all()
    return render_template("topic/new.html", bs=bs)


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
