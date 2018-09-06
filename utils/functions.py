import redis
from flask import session, redirect, url_for
from functools import wraps

from flask_session import Session

from app.models import db
from utils.settings import MYSQL_DATABASES, REDIS_DATABASE


def is_login(func):
    @wraps(func)
    def check_status(*args, **kwargs):
        try:
            user_id = session['user_id']
        except:
            return redirect(url_for('user.login'))
        return func(*args, **kwargs)
    return check_status


def init_ext(app):
    # 绑定app和db
    db.init_app(app)
    # 绑定session和app
    sess = Session()
    sess.init_app(app)


def get_mysqldb_url():
    driver = MYSQL_DATABASES['DRIVER']
    DH = MYSQL_DATABASES['DH']
    ROOT = MYSQL_DATABASES['ROOT']
    PASSWORD = MYSQL_DATABASES['PASSWORD']
    HOST = MYSQL_DATABASES['HOST']
    PORT = MYSQL_DATABASES['PORT']
    NAME = MYSQL_DATABASES['NAME']
    return '{}+{}://{}:{}@{}:{}/{}'.format(driver, DH, ROOT,
                                           PASSWORD, HOST, PORT, NAME)

def get_redisdb_url():
    host = REDIS_DATABASE['HOST']
    port = REDIS_DATABASE['PORT']
    return redis.Redis(host=host, port=port)
