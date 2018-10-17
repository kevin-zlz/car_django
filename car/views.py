from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,JsonResponse,response
import json
from . import models
from utils.tokenHelper import jwtEncoding,jwtDecoding
from werkzeug.security import generate_password_hash, check_password_hash
# Create your views here.
# 添加城市
def addcity(request):
    if request.method == 'POST':
        strict=set()
        with open('site.json', 'r',encoding='utf8') as fp:
            data1 = json.load(fp)
            for j in range(len(data1)):

                cityname=data1[j]['cityname']
                print(cityname)
                data=data1[j]['sites']
                for i in range(len(data['sites'])):
                    strict.add(data['sites'][i]['area'])
                strict_list=list(strict)
                for i in range(len(strict_list)):
                    city={
                        "cityname":cityname,
                        "strictname":strict_list[i]
                    }
                    uu = models.City.objects.create(**city)
        return JsonResponse({"code": "808"})
# 添加城市门店
def addcitystore(request):
    if request.method == 'POST':
        strict=set()
        with open('aa.json', 'r',encoding='utf-8') as fp:
            data1 = json.load(fp)
            print(data1)
            for j in range(len(data1)):
                print(data1[j])
                data = data1[j]['sites']

                for i in range(len(data['sites'])):
                    print(models.City.objects.filter(strictname=data['sites'][i]['area']).values('id'))
                    city={
                        "storename":data['sites'][i]['name'],
                        "detailaddress":data['sites'][i]['address'],
                        "storetel":data['sites'][i]['site_phone'],
                        "storetime":data['sites'][i]['from_time']+'-'+data['sites'][i]['to_time'],
                        "storeaddress_id": models.City.objects.filter(strictname=data['sites'][i]['area']).values('id')[0]['id']
                    }
                    uu = models.CityStore.objects.create(**city)
        return JsonResponse({"code": "808"})

# 查询通过城市编号查询城市门店
def querycitystore(request):
    city = {
        "cityname": "北京"
    }
    if request.method == 'POST':
        try:
            strictandstores=[]
            stricts = models.City.objects.filter(cityname=city['cityname']).values('strictname','id')
            for strict in stricts:
                stores=models.CityStore.objects.filter(id=strict['id']).values('storename','storetel','detailaddress','storetime')
                storelist=[]
                for store in stores:
                    storelist.append({
                        "storename":store['storename'],
                        "storetel":store['storetel'],
                        "detailaddress":store['detailaddress'],
                        "storetime":store['storetime']
                    })
                strictandstore={
                    "strictname":strict["strictname"],
                    "stores":storelist
                }
                strictandstores.append(strictandstore)
            # print(strictandstores)
            return JsonResponse({"code": "808"})
        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})
    pass

# 添加门店下的车辆
def addcartostore(request):
    pass

# 查询门店下面的可用汽车
def querycarbystore(request):
    pass

# 多条件查询汽车基本信息
def querycarbyconditions(request):
    pass

# 根据汽车id查询车辆详情
def querycardetailbyid(request):
    pass








