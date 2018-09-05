import os

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
# from flask.json import jsonify

from app.models import User, House, Area, Facility, HouseImage
from utils import status_code
from utils.functions import is_login
from utils.settings import HOUSE_DIR

house_blueprint=Blueprint('house',__name__)

@house_blueprint.route('my_house/')
def my_house():
    return render_template('myhouse.html')


@house_blueprint.route('house_info/')
@is_login
def house_info():
    #判断当前登录的用户是否实名认证，若已经认证，返回发布的房屋信息，
    user=User.query.get(session['user_id'])
    if user.id_card:
        #已经认证，返回房源信息
        houses = House.query.filter(House.user_id == session['user_id']).all()
        house_info = [house.to_dict() for house in houses]
        return jsonify({'code':200,'msg':'请求成功','house_info':house_info})
    else:
        # 未认证，
        return jsonify({'code':1013,'msg':'未实名认证'})


@house_blueprint.route('new_house/')
@is_login
def new_house():
    return render_template('newhouse.html')


@house_blueprint.route('area_facility/',methods=['GET'])
def area_facility():
    #获取所有地区
    areas=Area.query.all()
    #获取所有设施
    facilitys = Facility.query.all()
    #序列化
    facility_info =[facility.to_dict() for facility in facilitys]
    area_info = [area.to_dict() for area in areas]
    return jsonify(code=status_code.OK , facility_info=facility_info , area_info=area_info )


@house_blueprint.route('new_house/',methods=['POST'])
def my_new_house():
    #获取值，创建房屋信息,
    data = request.form

    house = House()
    house.user_id = session['user_id']
    house.title = data.get('title')
    house.price = data.get('price')
    house.area_id = data.get('area_id')
    house.address = data.get('address')
    house.room_count = data.get('room_count')
    house.acreage = data.get('acreage')
    house.unit = data.get('unit')
    house.capacity = data.get('capacity')
    house.beds = data.get('beds')
    house.deposit = data.get('deposit')
    house.max_days= data.get('max_days')
    house.min_days = data.get('min_days')

    #获取设施信息，使用getlist
    facilities = data.getlist('facility')
    for f_id in facilities:
        facility = Facility.query.get(f_id)
        #添加房屋和设施的关联关系，多对多
        house.facilities.append(facility)
    # commit 在数据库中创建house和设施的中间表数据
    house.add_update()
    del session['house_id']
    session['house_id']=house.id
    return jsonify(code=status_code.OK )


@house_blueprint.route('add_img/', methods=['POST'])
def add_img():
    house_id=session['house_id']
    img=request.files.get('house_image')
    if img:
        img.save(os.path.join(HOUSE_DIR,img.filename))

        houseimg=HouseImage()
        house_img_path=os.path.join('house',img.filename)

        houseimg.house_id=house_id
        houseimg.url=house_img_path
        houseimg.add_update()
        #首图：
        house = House.query.get(house_id)
        if not house.index_image_url:
            house.index_image_url = house_img_path
            house.add_update()


        # del session['house_id']
        return jsonify(code=status_code.OK,img_path=house_img_path)
    else:
        return jsonify({'code':1015,'msg':'请求失败'})


@house_blueprint.route('detail/',methods=['GET'])
def detail():
    return render_template('detail.html')


@house_blueprint.route('detail/<int:id>/',methods=['GET'])
@is_login
def house_detail(id):
    house = House.query.get(id)
    return jsonify(code=200,detail=house.to_full_dict())

@house_blueprint.route('booking/')
def booking():
    return render_template('booking.html')

