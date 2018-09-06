
import redis

from utils.functions import get_mysqldb_url, get_redisdb_url


class Config():
    # 配置数据库
    SQLALCHEMY_DATABASE_URI = get_mysqldb_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # session的配置
    SESSION_TYPE = 'redis'
    SESSION_REDIS = get_redisdb_url()

