import redis
from flask import Flask
from flask_session import Session

from app.house_view import house_blueprint
from app.models import db
from app.order_views import order_blueprint
from app.user_views import user_blueprint
from utils.config import Config
from utils.functions import init_ext
from utils.settings import STATIC_DIR, TEMPLATES_DIR


def create_app():

    app = Flask(__name__,
                static_folder=STATIC_DIR,
                template_folder=TEMPLATES_DIR)
    # 配置
    app.config.from_object(Config)
    # 注册蓝图
    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    app.register_blueprint(blueprint=house_blueprint, url_prefix='/house')
    app.register_blueprint(blueprint=order_blueprint, url_prefix='/order')
    # 初始化各种第三方库
    init_ext(app)

    return app