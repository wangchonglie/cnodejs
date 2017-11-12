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
    log('token1', token)
    csrf_tokens.add(token)
    board_id = int(request.args.get("board_id", 0))
    if board_id == 0:
        ms = Topic.all()
    else:
        ms1 = Topic.find_all(board_id=0)
        ms2 = Topic.find_all(board_id=board_id)
        ms = ms1 + ms2
    bs = Board.all()
    log('ms的值',ms)
    return render_template("topic/index.html", ms=ms, token=token, bs=bs)


@main.route("/<int:id>")
def detail(id):
    m = Topic.get(id)
    return render_template("topic/detail.html", topic=m)


@main.route("/new")
def new():
    bs = Board.all()
    return render_template("topic/new.html", bs=bs)


@main.route("/logout")
def logout():
    session['user_id'] = None
    return redirect(url_for('index.index'))


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
def delete():
    delete_id = int(request.args.get('id'))
    delete_name = Topic.find(delete_id)
    token = request.args.get('token')
    log('token2', token)
    u = current_user()
    log('u', u)
    log(token in csrf_tokens)
    log('csrf_tokens', csrf_tokens)
    if token in csrf_tokens:
        csrf_tokens.remove(token)
        log('1')
        if u is not None:
            delete_name.delete()
            log('reply',Reply.find_all(topic_id=delete_id))
            rs = Reply.find_all(topic_id=delete_id)
            for r in rs:
                r.delete()
                
            return redirect(url_for('.index'))
    else:
        log('没有删除权限')
        abort(403)
