from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse,JsonResponse,response
from datetime import datetime
import json
from . import models
from utils.tokenHelper import *
# 根据用户id查询用户参与的所有活动
def queryTravelByuid(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_TOKEN')
        decode = jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256'])
        if decode:
            telphone = decode['some']
            uid = models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
            jointravels = models.UserJoinTravel.objects.filter(joiner=uid).values('joinTravel__id')
            print(jointravels)
            travels=[]
            for jointraval in jointravels:
                travels.append(models.UserAriseTravel.objects.filter(id=jointraval['joinTravel__id']).order_by('-pubtime').values())
            print(travels)
            datas = []
            for travel in travels:
                travel=travel[0]
                routelist = []
                joinerlist=[]
                uu = models.TravelPlace.objects.filter(places_id=travel['id']).values()
                for i in uu:
                    routelist.append(i['address'])
                joiners = models.UserJoinTravel.objects.filter(joinTravel__id=travel['id']).values('joiner__uname')
                for j in joiners:
                    joinerlist.append(j['joiner__uname'])
                aa = models.CityIcon.objects.filter(cityname=travel['travelstartplace']).values('iconurl')[0]['iconurl']
                joinnum = len(models.UserJoinTravel.objects.filter(joinTravel__id=travel['id']).values())
                data = {
                    "initiator_id": travel['initiator_id'],
                    "province": travel['travelstartplace'],
                    "travelid": travel['id'],
                    "travelstrattime": travel['travelstrattime'],
                    "travelendtime": travel['travelendtime'],
                    "menbers": travel['menbers'],
                    "linkname": travel['linkname'],
                    "linknumber": travel['linknumber'],
                    "describe": travel['destribe'],
                    "routelist": routelist,
                    "cityicon": aa,
                    "joinnum": joinnum,
                    "joiners":joinerlist,
                }
                datas.append(data)
            print(datas)
            return JsonResponse(datas, safe=False)
    else:
        return JsonResponse({"statuscode": "402"})

# 根据用户id查询用户参与的已结束活动（根据活动结束时间查）
def queryJoinedTravel(request):
    if request.method == 'POST':
        try:
            now_time = datetime.now()
            # 结束时间小于当前时间travelendtime__lt=now_time
            data = models.UserJoinTravel.objects.filter(joiner_id=13,joinTravel__travelendtime__lt=now_time).values('joinTravel__travelstartplace', 'joinTravel__menbers', 'joinTravel__linkname','joinTravel__linknumber', 'joinTravel__travelstrattime','joinTravel__travelendtime','joinTravel__destribe')
            # data = models.UserAriseTravel.objects.filter(initiator=1,travelendtime__lt=now_time).values()
            for a in data:
                a["joinTravel__travelstrattime"]=a["joinTravel__travelstrattime"].strftime("%Y-%m-%d %H:%M:%S").split('+')[0]
                a["joinTravel__travelendtime"]=a["joinTravel__travelendtime"].strftime("%Y-%m-%d %H:%M:%S").split('+')[0]
            return HttpResponse(json.dumps(list(data),ensure_ascii=False))
        except Exception as ex:
            return JsonResponse({"statuscode": "401"})
    else:
        return JsonResponse({"statuscode": "402"})

# 根据用户id查询用户参与的未进行活动（根据活动开始时间查）
def queryNotJoinTravel(request):
    if request.method == 'POST':
        try:
            now_time = datetime.now()
            # 结束时间大于当前时间travelstrattime_gt=now_time
            data = models.UserJoinTravel.objects.filter(joiner_id=13, joinTravel__travelstrattime__gt=now_time).values('joinTravel__travelstartplace', 'joinTravel__menbers', 'joinTravel__linkname', 'joinTravel__linknumber','joinTravel__travelstrattime', 'joinTravel__travelendtime', 'joinTravel__destribe')
            for a in data:
                a["joinTravel__travelstrattime"]=a["joinTravel__travelstrattime"].strftime("%Y-%m-%d %H:%M:%S").split('+')[0]
                a["joinTravel__travelendtime"]=a["joinTravel__travelendtime"].strftime("%Y-%m-%d %H:%M:%S").split('+')[0]
            return HttpResponse(json.dumps(list(data),ensure_ascii=False))
        except Exception as ex:
            return JsonResponse({"statuscode": "401"})
    else:
        return JsonResponse({"statuscode": "402"})

# 根据用户id及活动id取消用户参与的未进行活动（根据活动开始时间查）
def cancelNotJoinTravel(request):
    if request.method == 'POST':
        try:
            token = request.META.get('HTTP_TOKEN')
            decode = jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256'])
            if decode:
                telphone = decode['some']
                uid = models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
                uu = json.loads(request.body)
                # menbers = uu['joinTravel__menbers']
                id = uu['joinTravel__id']
                affect_rows1 = models.UserJoinTravel.objects.filter(joinTravel__id=id).delete()
                return JsonResponse({"statuscode": "201"})
        except Exception as ex:
            return JsonResponse({"statuscode": "401"})
    else:
        return JsonResponse({"statuscode": "402"})

# 根据用户id查询用户发起的所有活动
def queryInitatorTravel(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_TOKEN')
        decode = jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256'])
        if decode:
            telphone = decode['some']
            uid = models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
            travels = models.UserAriseTravel.objects.filter(initiator__id=uid).order_by('-pubtime').values()
            datas = []
            for travel in travels:
                routelist = []
                joinerlist=[]
                uu = models.TravelPlace.objects.filter(places_id=travel['id']).values()
                for i in uu:
                    routelist.append(i['address'])
                joiners = models.UserJoinTravel.objects.filter(joinTravel__id=travel['id']).values('joiner__uname')
                for j in joiners:
                    joinerlist.append(j['joiner__uname'])
                aa = models.CityIcon.objects.filter(cityname=travel['travelstartplace']).values('iconurl')[0]['iconurl']
                joinnum = len(models.UserJoinTravel.objects.filter(joinTravel__id=travel['id']).values())
                data = {
                    "initiator_id": travel['initiator_id'],
                    "province": travel['travelstartplace'],
                    "travelid": travel['id'],
                    "travelstrattime": travel['travelstrattime'],
                    "travelendtime": travel['travelendtime'],
                    "menbers": travel['menbers'],
                    "linkname": travel['linkname'],
                    "linknumber": travel['linknumber'],
                    "describe": travel['destribe'],
                    "routelist": routelist,
                    "cityicon": aa,
                    "joinnum": joinnum,
                    "joiners":joinerlist,
                }
                datas.append(data)
            return JsonResponse(datas, safe=False)
    else:
        return JsonResponse({"statuscode": "402"})
# 添加一条UserAriseTravel记录
def addTraval(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_TOKEN')
        from datetime import datetime
        decode=jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256'])
        if decode:
            telphone = decode['some']
            uid = models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
            data = json.loads(request.body, encoding='utf-8')

            user = {
                "city_id":models.CityIcon.objects.filter(cityname=data['travalprovince']).values('id')[0]['id'],
                "initiator_id":uid,
                "travelstartplace":data['travalprovince'],
                "travelstrattime":data['travelstrattime'],
                "travelendtime":data['travelendtime'],
                "menbers":data['menbers'],
                "linkname":data['linkname'],
                "linknumber":data['linknumber'],
                "destribe":data['destribe'],
                "pubtime":datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            try:
                uu = models.UserAriseTravel.objects.create(**user)
                activityid=uu.id
                for i in data['travellist']:
                    line={
                        "places_id":activityid,
                        "address":i
                    }
                    bb=models.TravelPlace.objects.create(**line)
                return JsonResponse({"statuscode": "201"})
            except Exception as ex:
                return JsonResponse({"statuscode": "401"})
        else:
            return JsonResponse({"statuscode": "402"})

# 查询所有活动
def queryAllTravel(request):
    if request.method == 'POST':
        # try:
            travels=models.UserAriseTravel.objects.all().order_by('-pubtime').values()
            # travels=list(travels)

            datas=[]
            for travel in travels:
                routelist=[]

                uu=models.TravelPlace.objects.filter(places_id=travel['id']).values()

                for i in uu:
                    routelist.append(i['address'])
                aa=models.CityIcon.objects.filter(cityname=travel['travelstartplace']).values('iconurl')[0]['iconurl']
                joinnum=len(models.UserJoinTravel.objects.filter(joinTravel__id=travel['id']).values())
                data={
                    "initiator_id":travel['initiator_id'],
                    "province":travel['travelstartplace'],
                    "travelid":travel['id'],
                    "travelstrattime":travel['travelstrattime'],
                    "travelendtime":travel['travelendtime'],
                    "menbers":travel['menbers'],
                    "linkname":travel['linkname'],
                    "linknumber":travel['linknumber'],
                    "describe":travel['destribe'],
                    "routelist":routelist,
                    "cityicon":aa,
                    "joinnum":joinnum
                }
                datas.append(data)
            return JsonResponse(datas,safe=False)
        # except Exception as ex:
        #     return JsonResponse({"statuscode": "401"})
    else:
        return JsonResponse({"statuscode": "402"})

# 用户根据活动id参与活动
def joinTravelByid(request):
    from datetime import datetime
    if request.method == 'POST':
        try:
            token = request.META.get('HTTP_TOKEN')
            decode = jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256'])
            if decode:
                telphone = decode['some']
                uid = models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
                uu=json.loads(request.body)
                data={
                    "joiner_id":uid,
                    "joinTravel_id":uu['travalid'],
                    "jointime":datetime.now()
                }
                res=models.UserJoinTravel.objects.create(**data)
                return JsonResponse({"statuscode": "808"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"statuscode": "401"})
    else:
        return JsonResponse({"statuscode": "402"})

# 根据活动id删除用户活动
def deleteTravelByid(request):
    pass
