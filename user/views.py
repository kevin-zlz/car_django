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

