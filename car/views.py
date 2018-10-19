from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse, response
import json
from . import models
import random



# Create your views here.
# 添加城市
def addcity(request):
    if request.method == 'POST':
        strict = set()
        with open('site.json', 'r', encoding='utf8') as fp:
            data1 = json.load(fp)
            for j in range(len(data1)):

                cityname = data1[j]['cityname']
                print(cityname)
                data = data1[j]['sites']
                for i in range(len(data['sites'])):
                    strict.add(data['sites'][i]['area'])
                strict_list = list(strict)
                for i in range(len(strict_list)):
                    city = {
                        "cityname": cityname,
                        "strictname": strict_list[i]
                    }
                    uu = models.City.objects.create(**city)
        return JsonResponse({"code": "808"})


# 添加城市门店
def addcitystore(request):
    if request.method == 'POST':
        strict = set()
        with open('aa.json', 'r', encoding='utf-8') as fp:
            data1 = json.load(fp)
            print(data1)
            for j in range(len(data1)):
                print(data1[j])
                data = data1[j]['sites']

                for i in range(len(data['sites'])):
                    city = {
                        "storename": data['sites'][i]['name'],
                        "detailaddress": data['sites'][i]['address'],
                        "storetel": data['sites'][i]['site_phone'],
                        "storetime": data['sites'][i]['from_time'] + '-' + data['sites'][i]['to_time'],
                        "storeaddress_id":
                            models.City.objects.filter(strictname=data['sites'][i]['area']).values('id')[0]['id']
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
            strictandstores = []
            stricts = models.City.objects.filter(cityname=city['cityname']).values('strictname', 'id')
            for strict in stricts:
                stores = models.CityStore.objects.filter(id=strict['id']).values('storename', 'storetel',
                                                                                 'detailaddress', 'storetime')
                storelist = []
                for store in stores:
                    storelist.append({
                        "storename": store['storename'],
                        "storetel": store['storetel'],
                        "detailaddress": store['detailaddress'],
                        "storetime": store['storetime']
                    })
                strictandstore = {
                    "strictname": strict["strictname"],
                    "stores": storelist
                }
                strictandstores.append(strictandstore)
            # print(strictandstores)
            return JsonResponse(strictandstores,safe=False)
            # return JsonResponse({"code": "808"})
        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})
    pass


# 添加门店下的车辆
def addcartostore(request):
    if request.method == 'POST':
        strict = set()
        with open('carbase.json', 'r', encoding='utf8') as fp:
            data1 = json.load(fp)
            stores = models.CityStore.objects.all().values('id')
            for storeid in stores:
                for item in data1:
                    car = {
                        "carname": item['carname'],
                        "brand": item['brand'],
                        "cartype": item['cartype'],
                        "price": item['price'].split('元')[0],
                        "carid": creatCarId(),
                        "storeid_id": storeid['id']
                    }
                    models.CarBase.objects.create(**car)
        return JsonResponse({"code": 208})


def creatCarId():
    s = ['京', '沪', '津', '渝', '冀', '晋', '蒙', '辽', '吉', '黑', '苏', '浙', '皖', '闽', '赣']
    d = ['ABCEFHG', 'ABC', 'ABCE', 'ABCFGH', 'ABCDEFGHJRT', 'ABCDEFHJKLM', 'ABCDEFGHJKLM', 'ABCDEFGHJKLMNPV',
         'ABCDEFGHJ', 'ABCDEFGHJKLMNPR', 'ABCDEFGHJKLMN', 'ABCDEFGHJKL', 'ABCDEFGHJKLMNPQRS', 'ABCDEFGHJK',
         'ABCDEFGHJKLM']
    b = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    c = '0123456789'
    dic = {}
    for i in range(len(s)):
        dic[s[i]] = list(d[i])
    leg = ''.join(random.sample(b, 1))
    foot = ''.join(random.sample(c, 4))
    head = random.choice(list(dic))
    body = random.choice(dic[head])
    carid = head + body + leg + foot
    return carid

# 添加汽车详情
def addcardetail(request):
    try:
        if request.method == 'POST':
            carsbase=models.CarBase.objects.all().values('id','carname','price')
            carsbase=list(carsbase)
            # print(carsbase)
            with open('carsdetail_new.json', 'r',encoding='utf-8') as fp:
                cars=json.load(fp)


            for car in cars:
                for i in carsbase:
                    if car['carname']==i['carname'] and int(car['price'].split('元')[0])==i['price']:
                        res=models.CarDetail.objects.create(chexi=car['chexi'],niandaikuan=car['niandaikuan'],peizhikun=car['peizhikun'],sitenum=car['sitenum'],doornum=car['doornum'],oiltype=car['oitype'],changespeed=car['changespeed'],pailiang=car['pailiang'],oilnum=car['oilnum'],qudong=car['qudong'],jinqixingshi=car['jinqixingshi'],carwindow=car['carwindow'],oilcaptiy=car['oilcaptiy'],musicnum=car['musicnum'],sitetype=car['sitetype'],isdaocheleida=car['isdaocheleida'],isqinang=car['isqinang'],isdvd=car['isdvd'],isgps=car['isgps'],car_id=i['id'])

            return JsonResponse({"code": "808"})
    except Exception as ex:
        print(ex)
        return JsonResponse({"code":"408"})





# 查询门店下面的可用汽车
def querycarbystore(request):
    pass


# 多条件查询汽车基本信息

def querycarbyconditions(request):
    pass


# 根据汽车id查询车辆详情
def querycardetailbyid(request):
    # 测试数据:
    #     {
    #         "id":"2"
    #     }
    if request.method == 'POST':
        try:
            id = json.loads(request.body)['id']
            detail = models.CarDetail.objects.filter(car_id=id).values()
            detail = list(detail)[0]
            return JsonResponse(detail)
        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 根据城市查询门店
def queryStoresbycity(request):
    if request.method == 'POST':
        city={
            "cityname":"北京"
        }
        data=[]
        try:
            stricts=models.City.objects.filter(cityname=city['cityname']).values('id','strictname')
            for strict in stricts:
                strictplace={
                    "strictname":strict['strictname'],
                    "stores":[]
                }
                stores=models.CityStore.objects.filter(storeaddress=strict['id']).values('id','storename','storetel','storetime')
                for store in stores:
                    storeplace={
                        "storename":store['storename'],
                        "storetel":store['storetel'],
                        "storetime":store['storetime'],
                        "storeid":store['id']
                    }
                    strictplace['stores'].append(storeplace)
                data.append(strictplace)
            # print(data)
            return JsonResponse(data,safe=False)
        except Exception as ex:
            return JsonResponse({"code":"408"})

