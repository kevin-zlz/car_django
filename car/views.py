from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse, response
import json
from . import models
from user.models import UserOrder
import random
from django.db.models import Q
from django.db.models.aggregates import Count


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

    if request.method == 'POST':
        # try:
            cityname = json.loads(request.body)['cityname']
            strictandstores = []
            stricts = models.City.objects.filter(cityname=cityname).values('strictname', 'id')
            for strict in stricts:
                stores = models.CityStore.objects.filter(storeaddress__id=strict['id']).values('id','storename', 'storetel',
                                                                                 'detailaddress', 'storetime')
                storelist = []
                for store in stores:
                    storelist.append({
                        "id":store['id'],
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
            print(strictandstores)
            return JsonResponse(strictandstores,safe=False)
            # return JsonResponse({"code": "808"})
        # except Exception as ex:
        #     return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})
    # pass


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
    from  datetime import datetime
    if request.method == 'POST':
        # try:
            condition = json.loads(request.body)
            # print(condition)
            takestoreid=models.CityStore.objects.filter(storename=condition['takestore'],storeaddress__cityname=condition['takecityname']).values('id')[0]['id']
            # backstoreid=models.CityStore.objects.filter(storename=condition['backstore'],storeaddress__cityname=condition['backcityname']).values('id')[0]['id']
            # print(takestoreid,backstoreid)
        # Q(takecartime__gt=datetime.strptime(condition['backtime'],'%Y-%m-%d %H:%M:%S'))
        #     print(condition['backtime'])
        #     print(type(condition['backtime']))
        #     str1 = '2018-10-19'

            # 订单中不可用车辆
            order=UserOrder.objects.all().exclude(Q(returncartime__gte=datetime.strptime(condition['backtime'],'%Y-%m-%d %H:%M:%S'))|Q(takecartime__gt=datetime.strptime(condition['backtime'],'%Y-%m-%d %H:%M:%S'))).values('id','takecartime','returncartime','car__id')
            caridlist=[]
            index = condition['currentPage']
            pageCount = condition['pageCount']
            print('---------', index, pageCount)
            start = (index - 1) * pageCount
            end = index * pageCount - 1
            for o in order:
                caridlist.append(o['car__id'])
            print(caridlist)
            cars=models.CarBase.objects.exclude(id__in=caridlist).filter(storeid=takestoreid).values()[start:end]
            # print(cars)
            # return -0JsonResponse(strictandstores,safe=False)
            return JsonResponse(list(cars),safe=False)
        # except Exception as ex:
        #     return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 多条件查询汽车基本信息
def querycarbyconditions(request):
    from datetime import datetime
    if request.method == 'POST':
        # try:
        condition = json.loads(request.body)
        print(condition)
        takestoreid = models.CityStore.objects.filter(storename=condition['condition']['takestore'],
                                                      storeaddress__cityname=condition['condition']['takecityname']).values('id')[0][
            'id']
        backstoreid=models.CityStore.objects.filter(storename=condition['condition']['backstore'],storeaddress__cityname=condition['condition']['backcityname']).values('id')[0]['id']
        print(takestoreid,backstoreid)
        # Q(takecartime__gt=datetime.strptime(condition['backtime'],'%Y-%m-%d %H:%M:%S'))
        #     print(condition['backtime'])
        #     print(type(condition['backtime']))
        #     str1 = '2018-10-19'

        # 订单中不可用车辆
        order = UserOrder.objects.all().exclude(
            Q(returncartime__gte=datetime.strptime(condition['condition']['taketime'], '%Y-%m-%d %H:%M:%S')) | Q(
                takecartime__gt=datetime.strptime(condition['condition']['backtime'], '%Y-%m-%d %H:%M:%S'))).values('id',
                                                                                                       'takecartime',

                                                                                                       'returncartime',
                                                                                                       'car__id')
        print(order)
        caridlist = []
        for o in order:
            caridlist.append(o['car__id'])
        con = {}
        if condition['condition']['condition']['carPingpai']:
            con['brand__in']=condition['condition']['condition']['carPingpai']
        if condition['condition']['condition']['carLeixing']:
            con['cartype__in']=condition['condition']['condition']['carLeixing']
        if condition['condition']['condition']['carJiage']:
            con['price__lte']=int(condition['condition']['condition']['carJiage'])

        index=condition['condition']['currentPage']
        pageCount=condition['condition']['pageCount']
        print('---------',index,pageCount)
        start=(index-1)*pageCount
        end=index*pageCount-1
        # print(caridlist,condition['condition']['carPingpai'],condition['condition']['carLeixing'],int(condition['condition']['carJiage']))
        # cars = models.CarBase.objects.exclude(id__in=caridlist).filter(storeid=takestoreid).filter(brand__in=condition['condition']['condition']['carPingpai'],cartype__in=condition['condition']['condition']['carLeixing'],price__lte=int(condition['condition']['condition']['carJiage'])).values()
        cars = models.CarBase.objects.exclude(id__in=caridlist).filter(storeid=takestoreid).filter(**con).values()[start:end]
        print(cars)
        # return -0JsonResponse(strictandstores,safe=False)
        return JsonResponse(list(cars), safe=False)
    # except Exception as ex:
    #     return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})


# 根据汽车id查询车辆基本及详情信息
def querycarinfobyid(request):
    # 测试数据:
    #     {
    #         "id":"6"
    #     }
    if request.method == 'POST':
        try:
            info={}
            id = json.loads(request.body)['id']
            base=models.CarBase.objects.filter(id=id).values()
            detail = models.CarDetail.objects.filter(car_id=id).values()
            base=list(base)[0]
            detail = list(detail)[0]
            info['base']=base
            info['detail']=detail
            return JsonResponse(info,safe=False)
        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})


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

# 根据热门城市查询推荐车辆
def queryhotcar(request):
    if request.method == 'POST':
        # try:

            cityname = json.loads(request.body)['cityname']
            cars=UserOrder.objects.filter(takecarplace__storeaddress__cityname=cityname).values('car__carname','car__cardetail__sitenum','car__brand','car__cardetail__oilcaptiy').annotate(count=Count("car__carname")).order_by('-count')[0:6]
            print(cityname)
            print(cars)
            return JsonResponse(list(cars), safe=False)
        # except Exception as e:
        #     return JsonResponse({"code":408},safe=False)
    else:
        return JsonResponse({"code":608},safe=False)