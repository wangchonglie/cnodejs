import config
from flask import Flask


app = Flask(__name__)

app.secret_key = config.secret_key

#注册蓝图
from routes.index import main as index_routes
app.register_blueprint(index_routes)

if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=5000,
     )
    app.run(**config)