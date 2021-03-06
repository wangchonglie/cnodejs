import uuid
from routes import *
from flask import render_template, request, redirect, url_for, Blueprint, abort
from models.topic import Topic
from models.reply import Reply
from models.board import Board

main = Blueprint('topic', __name__)

csrf_tokens = set()


@main.route("/")
def index():
    u = current_user()
    bs = Board.all()
    tab = request.args.get('tab', 'all')
    page_no = int(request.args.get('pages', 1))
    board = Board.find_by(tab=tab)
    page_size = 15
    if tab == "all":
        filter_1 = {
            'deleted': False,
            'top': True,
            'board_id': {
                '$ne': 6
            }
        }
        ms1 = Topic.find_page(query_filter=filter_1, skip=page_size * (page_no - 1))
        filter_2 = {
            'deleted': False,
            'top': False,
            'board_id': {
                '$ne': 6
            }
        }
        if len(ms1) != 0:
            ms2 = Topic.find_page(query_filter=filter_2, page_size=15-len(ms1))
        else:
            ts = Topic.find_all(top=True)
            skip = page_size * (page_no - 1) - len(ts)
            ms2 = Topic.find_page(query_filter=filter_2, skip=skip)
        ms = ms1 + ms2
        # 每页15条数据，需要多少页
        pages = len(Topic.all()) / 15
        if isinstance(pages, float):
            pages += 1
        pages = int(pages)
    else:
        if board is not None:
            filter_1 = {
                'board_id': board.id,
                'deleted': False
            }
            ms = Topic.find_page(query_filter=filter_1)
        # 每页15条数据，需要多少页
        pages = len(Topic.find_all(board_id=board.id)) / 15
        if isinstance(pages, float):
            pages += 1
        pages = int(pages)
    return render_template("topic/index.html", pages=pages, user=u, ms=ms, bs=bs, tab=tab)


@main.route("/<int:id>")
def detail(id):
    u = current_user()
    token = str(uuid.uuid4())
    csrf_tokens.add(token)
    m = Topic.get(id)
    publish_time = Topic.new_time(m.created_time)
    return render_template("topic/detail.html", topic=m, token=token, timestamp=publish_time, user=u)


@main.route("/new")
def new():
    form = request.form
    bs = Board.all()
    return render_template("topic/new.html", bs=bs, form=form)


@main.route("/logout")
def logout():
    session.pop('user_id', '')
    return redirect(url_for('.index'))


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()
    m = Topic.new(form, user_id=u.id)
    return redirect(url_for('.detail', id=m.id))


@main.route("/delete")
@login_permission
def delete():
    delete_id = int(request.args.get('id'))
    delete_name = Topic.find(delete_id)
    token = request.args.get('token')
    u = current_user()
    if token in csrf_tokens:
        csrf_tokens.remove(token)
        if u is not None:
            delete_name.delete()
            rs = Reply.find_all(topic_id=delete_id)
            for r in rs:
                r.delete()
            return redirect(url_for('.index'))
    else:
        abort(403)


@main.route("/about")
def about():
    u = current_user()
    return render_template("topic/about.html", user=u)


@main.route("/top")
@admin_permission
def top():
    top_id = int(request.args.get('id'))
    topic = Topic.find(top_id)
    topic.top = True
    topic.save()
    return redirect(url_for('.detail', id=top_id))


@main.route("/top_undo")
@admin_permission
def top_undo():
    top_id = int(request.args.get('id'))
    topic = Topic.find(top_id)
    topic.top = False
    topic.save()
    return redirect(url_for('.detail', id=top_id))


