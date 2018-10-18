from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,response
from datetime import datetime
import json
from . import models
from utils.tokenHelper import jwtEncoding,jwtDecoding
from werkzeug.security import generate_password_hash, check_password_hash
# Create your views here.
# 用户登录
def login(request):
    data = json.loads(request.body)
    user = {
        "telphone": data['telphone'],
        "password": generate_password_hash(data['password'], method='pbkdf2:sha1:2000', salt_length=8)
    }
    if request.method == 'POST':
        try:
            u=models.UserBase.objects.filter(telephone=user['telphone']).values('password')
            print(u[0]['password'])
            print(data['password'])

            if u and check_password_hash(u[0]['password'], data['password']):
                result = {"code": "808"}
                resp = response.HttpResponse(json.dumps(result), status=200, charset='utf-8',
                                             content_type='application/json')
                resp['token'] = jwtEncoding(data['telphone'])
                resp['Access-Control-Expose-Headers'] = 'token'
                return resp
            else:
                return JsonResponse({"code": "404"})
        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 用户注册
def regist(request):
    data=json.loads(request.body)
    user = {
        "uname":data['uname'],
        "telephone": data['telephone'],
        "password": generate_password_hash(data['password'], method='pbkdf2:sha1:2000', salt_length=8),
        "pub_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "email":data['email']
    }
    if request.method == 'POST':
        try:
            result={"code": "808"}
            uu = models.UserBase.objects.create(**user)
            resp = response.HttpResponse(json.dumps(result), status=200, charset='utf-8',
                                         content_type='application/json')
            resp['token'] = jwtEncoding(data['telephone'])
            resp['Access-Control-Expose-Headers'] = 'token'
            return resp
        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})



    # print(check_password_hash(aa, password))

def personal(request):
    return HttpResponse(json.dumps({"code": 202}))
# 查询用户基本信息
def getuserbyid(request):
    return HttpResponse(json.dumps({"code": 202}))
# 添加用户详细信息
def adduserdetailbyid(request):
    return HttpResponse(json.dumps({"code": 202}))
# 更新用户手机号码
def updatetelbyid(request):
    return HttpResponse(json.dumps({"code": 202}))
# 更新用户密码
def updatepswbyid(request):
    return HttpResponse(json.dumps({"code": 202}))
# 更新用户详细信息
def updateuserdetailbyid(request):
    return HttpResponse(json.dumps({"code": 202}))
# 用户根据id查询所有订单
def queryOrder(request):
    if request.method == 'POST':
        try:
            token=request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone=jwtDecoding(token)['some']
                uid=models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
                uu=models.UserOrder.objects.filter(yonghu_id=uid).values('id','car__carname','takecarplace__detailaddress',
                                                                         'takecarplace__storeaddress__cityname','takecarplace__storeaddress__strictname',
                                                                         'takecartime','returncarplace__returncar__storeaddress__cityname',
                                                                         'returncarplace__returncar__storeaddress__strictname','returncarplace__returncar__detailaddress',
                                                                         'returncartime','orderstate__statename','ordertype__typename','car__price')
                return JsonResponse(list(uu),safe=False)
            else:
                return JsonResponse({"code":"408"})
        except Exception as e:
            return JsonResponse({"msg":e})


# 用户下订单
def addorder(request):
    if request.method == 'POST':
        try:
            token=request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone=jwtDecoding(token)['some']
                uid=models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
                order={
                    "yonghu_id":uid,
                    "car_id":1,
                    "takecarplace_id":2,
                    "takecartime":datetime.strptime('2018-10-16 10:00:00','%Y-%m-%d %H:%M:%S'),
                    "returncarplace_id":models.ReturnCar.objects.filter(returncar__id=3).values('id')[0]['id'],
                    "returncartime":datetime.strptime('2018-10-18 16:00:00','%Y-%m-%d %H:%M:%S'),
                    "orderstate_id":1,
                    "ordertype_id":1
                }
                uu=models.UserOrder.objects.create(**order)
                print(uu)
                return JsonResponse({"code":"208"})
            else:
                return JsonResponse({"code":"408"})
        except Exception as e:
            return JsonResponse({"msg":e})

# 添加还车表
def addReturnCar(request):
    if request.method == 'POST':
        stores=models.CityStore.objects.all().values('id')
        for store in stores:
            temp={
                "returncar_id":store['id']
            }
            models.ReturnCar.objects.create(**temp)
        return JsonResponse({"code":"208"})

