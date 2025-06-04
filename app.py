from flask import Flask, session, g  # g存储全局变量
from exts import db, mail
import config
from models import UserModel
from Ablueprint.qa import bp as qa_bp
from Ablueprint.auth import bp as auth_bp
from flask_migrate import Migrate
from flask import Flask
from exts import redis_client

app = Flask(__name__)

app.config.from_object(config)  # 导入config,自动读取配置信息文件

redis_client.init_app(app)

db.init_app(app)  # 启动后进行绑定
mail.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)


# hook 钩子函数 request前/后执行？如下面两个
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)
    g.user


@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__ == '__main__':
    app.run()
