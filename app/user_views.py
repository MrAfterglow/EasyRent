import random
import re
from flask import Blueprint, request, render_template, jsonify, session
import os
#导入模型
from app.models import db, User
from utils import status_code
#初始化蓝图
from utils.settings import UPLOAD_DIR
from utils.functions import is_login
user_blueprint=Blueprint('user',__name__)

@user_blueprint.route('create_all/')
def create_all():
    db.create_all()
    return '创建数据库中的表成功'

@user_blueprint.route('register/',methods=['GET'])
def register():
    if request.method=="GET":
        return render_template('register.html')

#获取验证码
@user_blueprint.route('img_code/',methods=['GET'])
def img_code():
    if request.method=="GET":
        s='123456789qwertyuiopasdfghjklzxcvbnm'
        code=''
        for i in range(4):
            code+=random.choice(s)
        # 将状态码code存在session
        session['code']=code
        # 返回json文件 用jsonify
        return jsonify({
            'code':200,
            'mgs':'请求成功',
            'data':code
        })

#注册
@user_blueprint.route('register/',methods=['POST'])
def my_register():
    if request.method=="POST":
        # 实现注册功能
        # 获取注册页面ajax提交过来的参数。request.form
        mobile=request.form.get('mobile')
        img_code=request.form.get('img_code')
        passwd=request.form.get('passwd')
        passwd2=request.form.get('passwd2')
        #校验参数是否完整
        if not all([mobile,img_code,passwd,passwd2]):
            return jsonify(status_code.USER_REGISTER_PARAMS_NOT_EXISTS)
        #校验手机号
        if not re.match(r'1[345678]\d{9}',mobile):
            return jsonify(status_code.USER_REGISTER_MOBILE_NOT_EXISTS)
        #校验图片验证码
        if session.get('code') != img_code:
            return jsonify()
        #校验密码是否一致
        if passwd != passwd2:
            return jsonify({'code': 200, 'msg': '两次密码不一致'})
        #验证手机号是否注册过
        user=User.query.filter(User.phone==mobile).all()
        if user:
            return jsonify({'code': 200, 'msg': '手机注册过'})
        user=User()
        user.phone=mobile
        user.name=mobile
        user.password=passwd
        user.add_update()
        return jsonify(status_code.SUCCESS)


#登录页面
@user_blueprint.route('login/',methods=['GET'])
def login():
    return render_template('login.html')


@user_blueprint.route('my_login/',methods=['GET'])
def my_login():
    if request.method=="GET":
        # 获取手机号和密码
        mobile = request.args.get('mobile')
        passwd = request.args.get('passwd')
        # 校验参数是否完整
        if not all([mobile,passwd]):
            return  jsonify(status_code.USER_LOGIN_NOT_ALL)
        # 校验手机号是否符合规格
        if not re.match(r'1[34567]\d{9}',mobile):
            return jsonify(status_code.USER_LOGIN_PHONE_IS_LOGIN_VALID)
        # 判断手机号是否存在
        user=User.query.filter(User.phone == mobile).first()
        if not user:
            return jsonify(status_code.USER_LOGIN_NOT_PHONE)
        # 校验密码是否正确
        if not user.check_pwd(passwd):
            return jsonify(status_code.USER_LOGIN_IS_NOT_PASSWD)
        # 记录用户登录成功：
        session['user_id'] = user.id
        return jsonify(status_code.SUCCESS)


# 返回my页面
@user_blueprint.route('my/',methods=['GET'])
@is_login
def my():
    return render_template('my.html')


# 个人信息
@user_blueprint.route('my_info/')
@is_login
def my_info():
    #获取session中的user_id
    user_id=session['user_id']
    user = User.query.get(user_id)
    user_info = user.to_basic_dict()
    return jsonify(user_info=user_info,code=200)


#退出 ，删除session中值：
@user_blueprint.route('logout/')
def logout():
    session.clear()
    return render_template('login.html')


#修改信息的页面：
@user_blueprint.route('profile/')
@is_login
def profile():
    return render_template('profile.html')

@user_blueprint.route('profile/',methods=['PATCH'])
@is_login
def my_profile():
    if request.method=="PATCH":
        #获取头像：
        avatar = request.files.get('avatar')
        user_id=session['user_id']
        if avatar:

            #保存图片到/static/media/upload/xxx.jpg
            avatar.save(os.path.join(UPLOAD_DIR,avatar.filename))
            #修改用户的头像字段：
            user = User.query.get(user_id)
            upload_avatar_path=os.path.join('upload',avatar.filename)
            user.avatar=upload_avatar_path
            user.add_update()
            return jsonify({'code':200,'msg':'请求成功 ', 'img_avatar':upload_avatar_path})
        else:
            return jsonify({'code':200,'msg':'没选头像'})



#修改用户名字：
@user_blueprint.route('change_name/',methods=['PATCH'])
@is_login
def change_name():
    if request.method=="PATCH":
        new_name=request.form.get('name')
        user_id=session['user_id']
        if new_name:
            user=User.query.get(user_id)
            user.name=new_name
            user.add_update()
            return jsonify({'code':200, 'msg': '请求成功'})


#返回实名认证页面
@user_blueprint.route('auth/')
def auth():

    return render_template('auth.html')


#
@user_blueprint.route('auth/',methods=['PATCH'])
def my_auth():
    #获取用户名和身份证号
    real_name=request.form.get('real_name')
    id_card=request.form.get('id_card')
    #校验完整
    if not all([real_name,id_card]):
        return jsonify({'code':1011,'msg':'请填写完整参数'})
    #校验身份证
    if not re.match(r'^[1-9]\d{16}[1-9X]$',id_card):
        return jsonify({'code':1012,'msg':'身份证号不符合规范'})
    #修改用户信息
    user=User.query.get(session['user_id'])
    user.id_card=id_card
    user.id_name=real_name
    user.add_update()
    return jsonify(status_code.SUCCESS)


#验证是否已经验证过身份证信息
@user_blueprint.route('auth_info/')
@is_login
def auth_info():
    user=User.query.get(session['user_id'])
    user_info=user.to_auth_dict()
    return jsonify({'code':200,'msg':'请求成功','user_info':user_info})