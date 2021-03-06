import config
from flask import Flask
from flask_ckeditor import CKEditor, CKEditorField
from flask import render_template
from datetime import timedelta


app = Flask(__name__)
ckeditor = CKEditor(app)
# 设置session过期时间
app.permanent_session_lifetime = timedelta(minutes=30)


@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


app.secret_key = config.secret_key
#注册蓝图
from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
from routes.mail import main as mail_routes
app.register_blueprint(index_routes)
app.register_blueprint(topic_routes, url_prefix='/topic')
app.register_blueprint(reply_routes, url_prefix='/reply')
app.register_blueprint(board_routes, url_prefix='/board')
app.register_blueprint(mail_routes, url_prefix='/mail')

if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=5000,
     )
    app.run(**config)