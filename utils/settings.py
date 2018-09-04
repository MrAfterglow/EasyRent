
import os

#基础路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#静态资源路径
STATIC_DIR = os.path.join(BASE_DIR, 'static')
#媒体路径
MEDIA_DIR = os.path.join(STATIC_DIR, 'media')
#图片路径
UPLOAD_DIR = os.path.join(MEDIA_DIR, 'upload')
HOUSE_DIR = os.path.join(MEDIA_DIR, 'house')
