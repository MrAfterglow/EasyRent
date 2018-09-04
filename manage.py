import redis as redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from app.house_view import house_blueprint
from app.models import db
from app.user_views import user_blueprint

app=Flask(__name__)
# MySQL配置
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:123456@127.0.0.1:3306/aj4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)
# 注册blueprint
app.register_blueprint(blueprint=user_blueprint,url_prefix='/user')
app.register_blueprint(blueprint=house_blueprint,url_prefix='/house')
# redis配置
app.config['SESSION_TYPE']='redis'
app.config['SESSION_REDSI']=redis.Redis(host='127.0.0.1',port=6379)
Session(app=app)




manage=Manager(app=app)

if __name__ == '__main__':
    manage.run()
