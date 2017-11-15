from flask import render_template, request, redirect, url_for, Blueprint, abort
from routes import *
from utils import log
from pymongo import MongoClient
from models.topic import Topic
from models.reply import Reply
from models.board import Board

main = Blueprint('topic', __name__)

import uuid
csrf_tokens = set()


@main.route("/")
def index():
    u = current_user()
    tab = request.args.get('tab', 'all')
    page_no = int(request.args.get('pages', 1))
    if tab == "all":
        log('debug')
        ms = Topic.find_page(page_no=page_no)
        # 每页15条数据，需要多少页
        pages = len(Topic.all()) / 15
        if isinstance(pages, float):
            pages += 1
        pages = int(pages)
        log('pages:', pages)
    else:
        board = Board.find_by(tab=tab)
        log('board', board)
        xianzhi = {
            'board_id': board.id,
        }
        ms = Topic.find_page(query_filter=xianzhi, page_no=page_no)
        # 每页15条数据，需要多少页
        pages = len(Topic.find_all(board_id=board.id)) / 15
        if isinstance(pages, float):
            pages += 1
        pages = int(pages)
    bs = Board.all()
    return render_template("topic/index.html", pages=pages, user=u, ms=ms, bs=bs, tab=tab)


@main.route("/<int:id>")
def detail(id):
    token = str(uuid.uuid4())
    csrf_tokens.add(token)
    m = Topic.get(id)
    return render_template("topic/detail.html", topic=m, token=token)


@main.route("/new")
def new():
    bs = Board.all()
    return render_template("topic/new.html", bs=bs)


@main.route("/logout")
def logout():
    session.pop('user_id')
    return redirect(url_for('.index'))


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
