from flask import render_template, request, redirect, url_for, Blueprint
from routes import *
from utils import log
from models.board import Board

main = Blueprint('board', __name__)


import uuid
csrf_tokens = set()


@main.route("/admin")
@admin_permission
def index():
    token = str(uuid.uuid4())
    csrf_tokens.add(token)
    bs = Board.all()
    return render_template('board/admin_index.html', bs=bs, token=token)


@main.route("/add", methods=["POST"])
@admin_permission
def add():
    form = request.form
    m = Board.new(form)
    return redirect(url_for('.index'))


@main.route("/delete")
@admin_permission
def delete():
    delete_id = int(request.args.get('id'))
    board_name = Board.find(delete_id)
    log(board_name)
    token = request.args.get('token')
    if token in csrf_tokens:
        csrf_tokens.remove(token)
        board_name.delete()
    return redirect(url_for('.index'))

