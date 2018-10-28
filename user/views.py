from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, response

import json
from . import models
from utils.tokenHelper import *
from werkzeug.security import generate_password_hash, check_password_hash
from car.models import CarDetail
from boke.models import Aritical
from traval.models import UserAriseTravel
from qiniu import Auth

# 产生随机数
import random
import time
from .miaodi import *
from django.db import connection
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
    print(user)
    if request.method == 'POST':
        # try:
            u = models.UserBase.objects.filter(telephone=user['telphone']).values('password')
            print(u)
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
        # except Exception as ex:
        #     return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 短信登陆
def Information(request):
    if request.method == "POST":
        now_dates = time.time()
        print(request.body)
        mobble = json.loads(request.body)
        mobbl = mobble['telephone']
        yecode = int(mobble["code"])
        print(yecode)
        try:
            cursor = connection.cursor()
            sql = "select * from securty WHERE telephone = {0}".format(mobbl)
            bb = cursor.execute(sql)
            res = cursor.fetchone()
            print(res)
            if (res[1] == yecode) and (float(res[2]) >= now_dates):
                sql = "UPDATE securty set state = 2 WHERE telephone = {0}".format(mobbl)
                bb = cursor.execute(sql)
                result = {"code": 0}
                resp = response.HttpResponse(json.dumps(result), status=200, charset='utf-8',content_type='application/json')
                resp['token'] = jwtEncoding(mobbl)
                resp['Access-Control-Expose-Headers'] = 'token'
                return resp
            else:
                return JsonResponse({"code": "408"})
        except Exception as ex:
            print(ex)
    else:
        return JsonResponse({"code": "408"})

# 用户注册
def regist(request):
    print("-------------------")
    data = json.loads(request.body)
    from datetime import datetime


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

# 查询用户详细信息
def queryuserdetail(request):

    if request.method == 'POST':
        # try:
            token = request.META.get('HTTP_TOKEN')
            decode = jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256'])
            if decode:
                telphone = decode['some']
                uid = models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
                user = models.UserDetail.objects.filter(yonghu__id=uid).values('realname','idcard','idcardtime','address','urgentname','urgenttel','yonghu__telephone','yonghu__email')
                return JsonResponse(list(user),safe=False)
        # except Exception as ex:
        #     return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 添加用户详细信息
def adduserdetailbyid(request):
    from datetime import datetime
    if request.method=='POST':
        try:
            token = request.META.get('HTTP_TOKEN')
            decode = jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256'])
            if decode:
                telphone = decode['some']
                uu = json.loads(request.body, encoding='utf-8')
                uid=models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
                user={
                    "realname":uu['realname'],
                    "idcard":uu['idcard'],
                    # "telephone":int(uu['telephone']),
                    "idcardtime":uu['idcardtime'],
                    "address":uu['address'],
                    "urgentname":uu['urgentname'],
                    "urgenttel":uu['urgenttel'],
                    "add_time":datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "yonghu_id":models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id'],
                    # "emile":uu["email"],
                }
                if len(models.UserDetail.objects.filter(yonghu__id=uid).values('id')):
                    res1=models.UserBase.objects.filter(id=models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']).update(telephone=uu['telephone'],email=uu["email"])
                    res=models.UserDetail.objects.filter(yonghu__id=uid).update(**user)
                else:
                    res1 = models.UserBase.objects.filter(
                        id=models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']).update(
                        telephone=uu['telephone'], email=uu["email"])
                    res = models.UserDetail.objects.create(**user)
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
    if request.method == 'POST':
        # try:
        bef_password = json.loads(request.body)['bef_password']
        aft_password = json.loads(request.body)['aft_password']
        token = request.META.get('HTTP_TOKEN')
        print(token)
        print("-----------------------------")

        print(jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256']))
        print("-----------------------------")
        if jwtDecoding(token):
            telphone = jwtDecoding(token)['some']
            password_old = models.UserBase.objects.filter(telephone=telphone).values('password')[0]['password']
            print(password_old)
            if check_password_hash(password_old,bef_password):
                res = models.UserBase.objects.filter(telephone=telphone).update(password=generate_password_hash(aft_password, method='pbkdf2:sha1:2000', salt_length=8))
                return JsonResponse({"code": "808"})
            else:
                JsonResponse({"code": "804"})
        else:
            JsonResponse({"code": "408"})
        # except Exception as ex:
        #     return JsonResponse({"code": "408"})
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
                data = json.loads(request.body)
                index = data['currentPage']
                pageCount = data['pageCount']
                start = (index - 1) * pageCount
                end = index * pageCount - 1
                uu = models.UserOrder.objects.filter(yonghu_id=uid).values('id', 'car__carname',
                                                                           'car__carid',
                                                                           'takecarplace__detailaddress',
                                                                           'takecarplace__storeaddress__cityname',
                                                                           'takecarplace__storeaddress__strictname',
                                                                           'takecartime',
                                                                           'returncarplace__returncar__storeaddress__cityname',
                                                                           'returncarplace__returncar__storeaddress__strictname',
                                                                           'returncarplace__returncar__detailaddress',
                                                                           'returncartime', 'orderstate__statename',
                                                                           'ordertype__typename', 'car__price','ordertype__id')[start:end]
                return JsonResponse(list(uu), safe=False)
            else:
                return JsonResponse({"code": "408"})
        except Exception as e:
            return JsonResponse({"msg": e})


# 根据取还车时间以及完成取消的条件查询
def queryOrderByCondithion(request):
    if request.method == 'POST':
        try:
            token = request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone = jwtDecoding(token)['some']
                data = json.loads(request.body)
                uid = models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
                condition={}
                condition['yonghu_id']=uid
                if data['fromtime'] and data['endtime']:
                    condition['add_time__lte']=data['endtime']
                    condition['add_time__gte']=data['fromtime']
                if data['statename']:
                    condition['orderstate__statename']=data['statename']

                index = data['currentPage']
                pageCount = data['pageCount']
                start = (index - 1) * pageCount
                end = index * pageCount
                print(data)
                uu = models.UserOrder.objects.filter(**condition).values('id', 'car__carname',
                                                                           'car__carid',
                                                                           'takecarplace__detailaddress',
                                                                           'takecarplace__storeaddress__cityname',
                                                                           'takecarplace__storeaddress__strictname',
                                                                           'takecartime',
                                                                           'returncarplace__returncar__storeaddress__cityname',
                                                                           'returncarplace__returncar__storeaddress__strictname',
                                                                           'returncarplace__returncar__detailaddress',
                                                                           'returncartime', 'orderstate__statename',
                                                                           'ordertype__typename', 'car__price',
                                                                           'ordertype__id')[start:end]
                return JsonResponse(list(uu), safe=False)
            else:
                return JsonResponse({"code": "408"})
        except Exception as e:
            return JsonResponse({"msg": e})

# 用户下订单
def addorder(request):
    from datetime import datetime
    if request.method == 'POST':
        try:
            token = request.META.get('HTTP_TOKEN')
            data = json.loads(request.body)
            print(data)
            if jwtDecoding(token):
                telphone = jwtDecoding(token)['some']
                uid = models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
                order = {
                    "yonghu_id": uid,
                    "car_id": data['carid'],
                    "takecarplace_id": data['takestoreid'],
                    "takecartime": datetime.strptime(data['taketime'], '%Y-%m-%d %H:%M:%S'),
                    "returncarplace_id": models.ReturnCar.objects.filter(returncar__id=data['backstoreid']).values('id')[0]['id'],
                    "returncartime": datetime.strptime(data['backtime'], '%Y-%m-%d %H:%M:%S'),
                    "orderstate_id": int(data['orderstate']),
                    "ordertype_id": int(data['ordertype']),
                }
                uu = models.UserOrder.objects.create(**order)
                # 修改车的所属门店
                dd= models.CarBase.objects.filter(id=data['carid']).update(storeid__id=data['backstoreid'])
                return JsonResponse({"code": "208"})
            else:
                return JsonResponse({"code": "408"})
        except Exception as e:
            return JsonResponse({"msg": e})


# 查看订单详情
def orderdetail(request):
    if request.method == 'POST':
        try:
            token = request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone = jwtDecoding(token)['some']
                data = json.loads(request.body)
                orderinfo=models.UserOrder.objects.filter(id=data['orderid']).values('car__id','car__price','car__carname','car__brand','yonghu__telephone','yonghu__userdetail__realname','yonghu__userdetail__idcard',
                                                                                     'yonghu__email','takecarplace__storeaddress__cityname','takecartime','takecarplace__detailaddress','takecarplace__storeaddress__id',
                                                                                     'returncarplace__returncar__storeaddress__cityname','returncarplace__returncar__detailaddress','returncartime','returncarplace__returncar__storeaddress__id'
                                                                                    )
                cardetail=CarDetail.objects.filter(id=orderinfo[0]['car__id']).values()
                all={
                    "orderinfo":list(orderinfo),
                    "carinfo":list(cardetail)
                }
                return JsonResponse(all,safe=False)
            else:
                return JsonResponse({"code": "408"})
        except Exception as e:
            return JsonResponse({"msg": e})

# 付款
def paymoney(request):
    if request.method == 'POST':
        try:
            token = request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone = jwtDecoding(token)['some']
                data = json.loads(request.body)
                uu=models.UserOrder.objects.filter(id=data['orderid']).update(orderstate_id=1)
                return JsonResponse({"code": "208"}, safe=False)
            else:
                return JsonResponse({"code": "408"})
        except Exception as e:
            return JsonResponse({"msg": e})

# 取消订单付款
def cancelorder(request):
    if request.method == 'POST':
        try:
            token = request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone = jwtDecoding(token)['some']
                data = json.loads(request.body)
                uu=models.UserOrder.objects.filter(id=data['orderid']).update(orderstate_id=2)
                return JsonResponse({"code": "208"}, safe=False)
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
            # print('1111',name)
            fname = '%s/pic/%s' %(settings.STATICFILES_DIRS[0],name)
            # print(fname)
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
        # print("=====================",token)
        try:
            tokenMsg = jwt.decode(str(token).encode(), SECRECT_KEY, audience='webkit', algorithms=['HS256'])
            data = json.loads(request.body)
            telephpne = tokenMsg['some']
            Positive = data['Positive']
            otherSide = data['otherSide']
            id1 = models.UserBase.objects.filter(telephone=telephpne).values('id')
            id = list(id1)[0]['id']
            data1 = {
                "face":Positive,
                "back":otherSide,
                "driver_id":id
            }
            res = models.UserDriver.objects.create(**data1)
            # print('000000',id)
            # print(2222222,Positive)
            # print(3333333, otherSide)
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
        token = request.META.get('HTTP_TOKEN')
        try:
            tokenMsg = jwt.decode(str(token).encode(), SECRECT_KEY, audience='webkit', algorithms=['HS256'])
            telephpne = tokenMsg['some']
            # 此处可以接收文件和字符串
            f1 = request.FILES['usericon']
            # 设置保存的文件名
            name = str(uuid.uuid4())+"."+f1.name.split('.')[1]
            print(name)
            fname = '%s/pic/%s' %(settings.STATICFILES_DIRS[0],name)
            # print(fname)
            # 由于文件是二进制流的方式，所有要用chunks()
            with open(fname, 'wb') as pic:
                for c in f1.chunks():
                    pic.write(c)
            res1 = models.UserIcon.objects.create(iconurl=name)
            id1 = models.UserIcon.objects.filter(iconurl=name).values('id')
            id = list(id1)[0]['id']
            res = models.UserBase.objects.filter(telephone=telephpne).update(icon_id=id)
            return JsonResponse({"code": 0,"name":name})
        except Exception as ex:
            print(ex)
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})


#  获取用户头像
def GetHead(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_TOKEN')
        # try:
        tokenMsg = jwt.decode(token.encode('utf-8'), SECRECT_KEY, audience='webkit', algorithms=['HS256'])
        telephpne = tokenMsg['some']

        url1 = models.UserBase.objects.filter(telephone=telephpne).values('icon__iconurl','uname')
        url = list(url1)[0]['icon__iconurl']
        uname=list(url1)[0]['uname']
        return JsonResponse({"code": 0,"url":url,"uname":uname})
        # except Exception as ex:
        #     print(ex)
        #     return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})



# 短信验证获取验证码-----------------------------

def SendCode(request):
    '''
    :param          mobile
    :return:        (1): code:412       手机号码输入不正确，或者已被注册
                    (2): code:200       发送短信成功
    '''


    # print(now_date + 60)
    #
    # timeArray = time.localtime(now_date)
    #
    # otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
    #
    # print(otherStyleTime)

    if request.method == "POST":

        mobble = json.loads(request.body)
        mobble=int(mobble['telephone'])
        print(mobble)#验证表单
        # if form.validate():
        #
        code=random.randrange(1000,9999)
        code=str(code)
        print(code)
        smsContent='【长安租车】您的验证码为{0}，请于{1}分钟内正确输入，如非本人操作，请忽略此短信。'.format(code,2)
        sendIndustrySms(mobble,smsContent)
        # sendIndustrySms(mobble,smsContent)
        # #将获取到的验证码存储到数据库中
        now_date = time.time() + 120;
        cursor = connection.cursor()
        sql = "DELETE from securty WHERE telephone = {0}".format(mobble)
        n = cursor.execute(sql)
        sql = "insert into securty() VALUE({0},{1},{2},{3})".format(mobble,code,now_date,1)
        bb = cursor.execute(sql)
        return JsonResponse({'code': 200, 'message': '发送成功'})
        # else:
        #     message = form.errors.popitem()[1][0]                 #弹出第一条验证失败错误信息
        #     print(type(jsonify({'code':406})))
        #     return JsonResponse({'code':412,'message':message})
        # response=JsonResponse({'code':200,'message':'发送成功'})
        # response['Access-Control-Allow-Origin']='*'
    else:
        return JsonResponse({"code": "408"})
#  验证验证码
def Verification(request):
    if request.method == "POST":
        now_dates = time.time()

        mobble = json.loads(request.body)

        mobbl = int(mobble['telephone'])
        yecode = int(mobble["code"])

        print(yecode)
        try:
            cursor = connection.cursor()

            sql = "select * from securty WHERE telephone = {0}".format(mobbl)

            bb = cursor.execute(sql)

            res = cursor.fetchone()
            print(res)

            if (res[1] == yecode) and (float(res[2]) >= now_dates):

                sql = "UPDATE securty set state = 2 WHERE telephone = {0}".format(mobbl)
                bb = cursor.execute(sql)
                r = {"code":0}
            else:
                r = {"code":403}

            return JsonResponse(r)

        except Exception as ex:
            print(ex)
    else:
        return JsonResponse({"code": "408"})

# ----------------------------------------

# 修改密码
def UpDataPwd(request):
    if request.method == "POST":
        mobble = json.loads(request.body)
        print(mobble)
        telephone = int(mobble['telephone'])
        password = mobble['password3']
        try:
            res = models.UserBase.objects.filter(telephone=telephone).update(password=generate_password_hash(password, method='pbkdf2:sha1:2000', salt_length=8))
            return JsonResponse({"code": 0})
        except Exception as ex:
            print(ex)
    else:
        return JsonResponse({"code": "408"})

# 图片上传
def qiniutoken(request):
    if request.method == 'GET':
        try:
            # 需要填写你的 Access Key 和 Secret Key
            access_key = 'egyqe8AdZTO3WyJj5no_isrVvmPfChCf4gRagdGf'
            secret_key = 'hUSk9xf7k0SSbtYqPLT_k3wLNjNDlMpF_xQiEXHm'
            filename = request.GET.get('key')
            print(filename)
            # 构建鉴权对象
            q = Auth(access_key, secret_key)
            # 要上传的空间
            bucket_name = 'changanzuche'
            key = str(uuid.uuid4()) + '.' + filename.split('.')[1]
            # 生成上传 Token，可以指定过期时间等
            token = q.upload_token(bucket_name, key, 3600)
            # 此处要写加入数据库代码
            domain = 'http://ph9cbg5cu.bkt.clouddn.com/'
            return JsonResponse({"uptoken": token, "domain": domain, "key": key})
        except Exception as ex:
            print('error-------------------------')
            print(ex)
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 根据用户号码查询订单数,文章数，活动数
def getcount(request):
    if request.method == 'POST':
        try:
            token = request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone = jwtDecoding(token)['some']
                ordercount=models.UserOrder.objects.filter(yonghu__telephone=telphone).values('id').count()
                articalcount=Aritical.objects.filter(yonghu__telephone=telphone).values('id').count()
                acitivecount=UserAriseTravel.objects.filter(initiator__telephone=telphone).values('id').count()
                print(ordercount,articalcount,acitivecount)
                return JsonResponse({"ordercount": ordercount,"artcount":articalcount,"actcount":acitivecount},safe=False)
            else:
                return JsonResponse({"code": "408"})
        except Exception as e:
            return JsonResponse({"msg": e})
