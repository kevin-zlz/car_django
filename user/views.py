from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response
from datetime import datetime

import json
from . import models
from utils.tokenHelper import *
from werkzeug.security import generate_password_hash, check_password_hash

# ------------------------------
import uuid
import car_django.settings as settings
# -----------------------------

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
            u = models.UserBase.objects.filter(telephone=user['telphone']).values('password')
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
    data = json.loads(request.body)
    user = {
        "uname": data['uname'],
        "telephone": data['telephone'],
        "password": generate_password_hash(data['password'], method='pbkdf2:sha1:2000', salt_length=8),
        "pub_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "email": data['email']
    }
    print(user)
    if request.method == 'POST':
        try:
            result = {"code": "808"}
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
# 测试数据:
    # {
    # 	"id":"1",
    # }

    id= json.loads(request.body)['id']

    if request.method == 'POST':
        try:
            userbase = models.UserBase.objects.filter(id=id).values('uname', 'telephone', 'password', 'icon',
                                                                    'pub_time', 'email')
            userbase = list(userbase)[0]
            user = {}
            user['id'] = id
            user['uname'] = userbase['uname']
            user['telephone'] = userbase['telephone']
            user['password'] = userbase['password']
            user['icon_id'] = userbase['icon']
            user['pub_time'] = userbase['pub_time']
            user['email'] = userbase['email']
            return JsonResponse(user)
        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})


# 添加用户详细信息
def adduserdetailbyid(request):
# 测试数据:
    #   {
    #     "realname":"王俊垚",
    #     "idcard":"232303199901010510",
    #     "idcardtime":"2020-10-10",
    #     "address":"苏州",
    #     "urgentname":"王羲之",
    #     "urgenttel":"13100886666",
    #     "yonghu_id":"1"
    #   }
    if request.method=='POST':
        try:
            uu=json.loads(request.body)


            user={
                "realname":uu['realname'],
                "idcard":uu['idcard'],
                "idcardtime":datetime.strptime(uu['idcardtime'],'%Y-%m-%d'),
                "address":uu['address'],
                "urgentname":uu['urgentname'],
                "urgenttel":uu['urgenttel'],
                "add_time":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "yonghu_id":uu['yonghu_id']
            }
            res=models.UserDetail.objects.create(**user)
            return JsonResponse({"code":"808"})

        except Exception as ex:
            print(ex)
            return JsonResponse({"node":"408"})
    else:
        return JsonResponse({"code":"404"})
# 更新用户手机号码
def updatetelbyid(request):

# 测试数据:
    #     {
    #       "id":"1",
    #       "bef_telephone": "110",
    #       "aft_telephone": "15999998888"
    #     }
    id= json.loads(request.body)['id']
    bef_telephone= json.loads(request.body)['bef_telephone']
    aft_telephone= json.loads(request.body)['aft_telephone']

    if request.method == 'POST':
        try:
            telephone_old = models.UserBase.objects.filter(id=id).values('telephone')
            telephone_old=list(telephone_old)[0]['telephone']

            if bef_telephone==telephone_old:
                res = models.UserBase.objects.filter(id=id).update(telephone=aft_telephone)

                return JsonResponse({"code": "808"})
            else:
                JsonResponse({"code": "408"})

        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})


# 更新用户密码
def updatepswbyid(request):
# 测试数据:
    # {
    #     "id": "1",
    #     "bef_password": "123456",
    #     "aft_password": "666666"
    # }
    id= json.loads(request.body)['id']
    bef_password= json.loads(request.body)['bef_password']
    aft_password= json.loads(request.body)['aft_password']
    if request.method == 'POST':
        try:
            password_old = models.UserBase.objects.filter(id=id).values('password')
            password_old=list(password_old)[0]['password']

            if bef_password==password_old:
                res = models.UserBase.objects.filter(id=id).update(password=aft_password)

                return JsonResponse({"code": "808"})
            else:
                JsonResponse({"code": "408"})

            return JsonResponse({"code": "808"})
        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 更新用户详细信息
def updateuserdetailbyid(request):
# 测试数据:
    # {
    #     "realname":"周杰伦",
    #     "idcard":"232303199901010510",
    #     "idcardtime":"2020-10-10",
    #     "address":"台湾",
    #     "urgentname":"小公举",
    #     "urgenttel":"13100886666",
    #     "yonghu_id":"1"
    # }
    userdetail=json.loads(request.body)
    id= json.loads(request.body)['yonghu_id']
    if request.method == 'POST':
        try:
            bef_detail = models.UserDetail.objects.filter(yonghu_id=id).values('realname', 'idcard', 'idcardtime', 'address',
                                                                    'urgentname', 'urgenttel','yonghu_id')
            bef_detail=list(bef_detail)[0]
            idcardtime=bef_detail['idcardtime'].strftime('%Y-%m-%d')
            bef_detail['idcardtime']=idcardtime
            bef_detail['yonghu_id']=str(bef_detail['yonghu_id'])
            print(userdetail,bef_detail)
            if userdetail!=bef_detail:
                res=models.UserDetail.objects.filter(yonghu_id=id).update(**userdetail)


                return JsonResponse({"code":"808"})
            else:
                return JsonResponse({"code": "408"})
        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})




# 用户根据id查询所有订单
def queryOrder(request):
    if request.method == 'POST':
        try:
            token = request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone = jwtDecoding(token)['some']
                uid = models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
                uu = models.UserOrder.objects.filter(yonghu_id=uid).values('id', 'car__carname',
                                                                           'takecarplace__detailaddress',
                                                                           'takecarplace__storeaddress__cityname',
                                                                           'takecarplace__storeaddress__strictname',
                                                                           'takecartime',
                                                                           'returncarplace__returncar__storeaddress__cityname',
                                                                           'returncarplace__returncar__storeaddress__strictname',
                                                                           'returncarplace__returncar__detailaddress',
                                                                           'returncartime', 'orderstate__statename',
                                                                           'ordertype__typename', 'car__price')
                return JsonResponse(list(uu), safe=False)
            else:
                return JsonResponse({"code": "408"})
        except Exception as e:
            return JsonResponse({"msg": e})


# 用户下订单
def addorder(request):
    if request.method == 'POST':
        try:
            token = request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone = jwtDecoding(token)['some']
                uid = models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
                order = {
                    "yonghu_id": uid,
                    "car_id": 1,
                    "takecarplace_id": 2,
                    "takecartime": datetime.strptime('2018-10-16 10:00:00', '%Y-%m-%d %H:%M:%S'),
                    "returncarplace_id": models.ReturnCar.objects.filter(returncar__id=3).values('id')[0]['id'],
                    "returncartime": datetime.strptime('2018-10-18 16:00:00', '%Y-%m-%d %H:%M:%S'),
                    "orderstate_id": 1,
                    "ordertype_id": 1
                }
                uu = models.UserOrder.objects.create(**order)
                print(uu)
                return JsonResponse({"code": "208"})
            else:
                return JsonResponse({"code": "408"})
        except Exception as e:
            return JsonResponse({"msg": e})


# 添加还车表
def addReturnCar(request):
    if request.method == 'POST':
        stores = models.CityStore.objects.all().values('id')
        for store in stores:
            temp = {
                "returncar_id": store['id']
            }
            models.ReturnCar.objects.create(**temp)
        return JsonResponse({"code": "208"})


# 上传驾照
def DicLoad(request):
    if request.method == 'POST':
        try:
            # 此处可以接收文件和字符串
            f1 = request.FILES['usericon']
            # 设置保存的文件名
            name=str(uuid.uuid4())+"."+f1.name.split('.')[1]
            print('1111',name)
            fname = '%s/pic/%s' %(settings.STATICFILES_DIRS[0],name)
            print(fname)
            # 由于文件是二进制流的方式，所有要用chunks()
            with open(fname, 'wb') as pic:
                for c in f1.chunks():
                    pic.write(c)
            # 驾照背面
            return JsonResponse({"name": name})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "407"})
    else:
        return JsonResponse({"code": "408"})

# 获取驾驶证正反图名字
def FlieName(request):
    if request.method == 'POST':
        # try:
        token = request.META.get('HTTP_TOKEN')
        print("=====================",token)
        try:
            tokenMsg = jwt.decode(str(token).encode(), SECRECT_KEY, audience='webkit', algorithms=['HS256'])
            data = json.loads(request.body)
            telephpne = tokenMsg['some']
            Positive = data['Positive']
            otherSide = data['otherSide']
            data1 = {

            }
            # print('000000',telephpne)
            # print(2222222, data['Positive'])
            # print(3333333, data['otherSide'])
            return JsonResponse({"code": "808"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "409"})
    else:
        return JsonResponse({"code": "4010"})

        # telphone = jwtDecoding(token.encode())['some']



# 修改头像
def UpHead(request):
    if request.method == 'POST':
        try:
            # 此处可以接收文件和字符串
            f1 = request.FILES['usericon']
            # 设置保存的文件名
            fname = '%s/pic/%s' %(settings.STATICFILES_DIRS[0],str(uuid.uuid4())+"."+f1.name.split('.')[1])
            print(fname)
            # 由于文件是二进制流的方式，所有要用chunks()
            with open(fname, 'wb') as pic:
                for c in f1.chunks():
                    pic.write(c)
            # 驾照背面

            return JsonResponse({"code": "808"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})
