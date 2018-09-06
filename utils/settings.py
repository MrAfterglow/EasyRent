
import os

#基础路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#templates路径
TEMPLATES_DIR = os.path.join(BASE_DIR,'templates')
#静态资源路径
STATIC_DIR = os.path.join(BASE_DIR, 'static')
#媒体路径
MEDIA_DIR = os.path.join(STATIC_DIR, 'media')
#图片路径
UPLOAD_DIR = os.path.join(MEDIA_DIR, 'upload')
HOUSE_DIR = os.path.join(MEDIA_DIR, 'house')

#数据库配置：
MYSQL_DATABASES = {
    'DRIVER' : 'mysql',
    'DH': 'pymysql',
    'ROOT': 'root',
    'PASSWORD': '123456',
    'HOST': '127.0.0.1',
    'PORT': 3306,
    'NAME': 'aj4'
}

REDIS_DATABASE = {
    'HOST':'127.0.0.1',
    'PORT': 6379
}
