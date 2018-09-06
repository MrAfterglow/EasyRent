from datetime import datetime
import random
import re
from flask import Blueprint, request, render_template, jsonify, session
import os
#导入模型
from app.models import db, User, House, Area
from utils import status_code
#初始化蓝图
from utils.settings import UPLOAD_DIR
from utils.functions import is_login
from app.models import Order

order_blueprint = Blueprint('order' ,__name__)

@order_blueprint.route('order/',methods=['POST'])
@is_login
def order():

    # 创建订单模型
    # 1.获取开始和结束时间
    begin_date=request.form.get('begin_date')
    end_date=request.form.get('end_date')

    begin_date = datetime.strptime(begin_date,'%Y-%m-%d')
    end_date=datetime.strptime(end_date,'%Y-%m-%d')
    # 2.获取当前用户和房屋id
    user_id = session['user_id']
    house_id = request.form.get('house_id')
    house = House.query.get(house_id)

    order=Order()
    order.user_id=user_id
    order.house_id = house_id
    order.begin_date = begin_date
    order.end_date = end_date
    order.days = (end_date - begin_date).days + 1
    order.house_price = house.price
    order.amount = order.days * house.price
    order.add_update()

    return  jsonify(code=200)

@order_blueprint.route('order/',methods=['GET'])
def orders():

    return render_template('orders.html')


@order_blueprint.route('order_info/')
@is_login
def order_info():

    orders = Order.query.filter(Order.user_id==session['user_id'])
    orders_info = [order.to_dict() for order in orders]

    return jsonify(code=200,orders_info=orders_info)


@order_blueprint.route('lorders/')
def lorders():
    return render_template('lorders.html')

@order_blueprint.route('lorder_info/')
def lorder_info():
    #获取别人对自己房屋下单的订单信息
    # 先查询自己发布的房屋信息：
    houses = House.query.filter(House.user_id==session['user_id'])
    house_ids = [house.id for house in houses]
    # 查询订单：
    orders = Order.query.filter(Order.house_id.in_(house_ids))
    lorder_info = [order.to_dict() for order in orders]
    return jsonify(code = 200 ,lorder_info=lorder_info)


@order_blueprint.route('o_status/',methods=['PATCH'])
def order_status():
    # 接收订单的id
    order_id=request.form.get('order_id')
    status = request.form.get('status')
    comment = request.form.get('commit')
    # 获取订单对象
    order = Order.query.get(order_id)
    order.status = status
    if comment:
        order.comment = comment
    order.add_update()
    return jsonify(status_code.SUCCESS)


@order_blueprint.route('hindex/')
def my_index():
    username = ''
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        username = user.name
    #获取房屋的轮播图
    houses = House.query.filter(House.index_image_url != '').order_by('-id')[:3]
    house_info = [house.to_dict() for house in houses]

    return jsonify(code = 200 ,username = username ,house_info = house_info)



@order_blueprint.route('search/')
def search():
    return render_template('search.html')


