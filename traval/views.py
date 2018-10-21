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
        # try:
            data = models.UserJoinTravel.objects.filter(joiner_id=13).values('joinTravel__travelstartplace','joinTravel__menbers','joinTravel__linkname','joinTravel__linknumber','joinTravel__travelstrattime','joinTravel__travelendtime','joinTravel__destribe')
            print(data)
            for a in data:
                a["joinTravel__travelstrattime"]=a["joinTravel__travelstrattime"].strftime("%Y-%m-%d %H:%M:%S").split('+')[0]
                a["joinTravel__travelendtime"]=a["joinTravel__travelendtime"].strftime("%Y-%m-%d %H:%M:%S").split('+')[0]
            return HttpResponse(json.dumps(list(data),ensure_ascii=False))
        # except Exception as ex:
        #     return JsonResponse({"statuscode": "401"})
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
            now_time = datetime.now()
            # 结束时间大于当前时间travelstrattime_gt=now_time
            data = models.UserJoinTravel.objects.filter(joiner_id=13, joinTravel__travelstrattime__gt=now_time).values('joinTravel__menbers','joinTravel__id')
            print(data)
            uu = list(data)[0]
            menbers = uu['joinTravel__menbers']
            id = uu['joinTravel__id']
            newmenbers = menbers-1
            affect_rows = models.UserAriseTravel.objects.filter(id=id).update(menbers=newmenbers)
            affect_rows1 = models.UserJoinTravel.objects.filter(joinTravel__id=id).delete()
            return JsonResponse({"statuscode": "201"})
        except Exception as ex:
            return JsonResponse({"statuscode": "401"})
    else:
        return JsonResponse({"statuscode": "402"})

# 根据用户id查询用户发起的所有活动
def queryInitatorTravel(request):
    if request.method == 'POST':
        try:
            data = models.UserAriseTravel.objects.filter(initiator_id=2).values()
            for a in data:
                a["travelstrattime"] = a["travelstrattime"].strftime("%Y-%m-%d %H:%M:%S").split('+')[0]
                a["travelendtime"] = a["travelendtime"].strftime("%Y-%m-%d %H:%M:%S").split('+')[0]
                a["pubtime"] = a["pubtime"].strftime("%Y-%m-%d %H:%M:%S").split('+')[0]
            return HttpResponse(json.dumps(list(data), ensure_ascii=False))
        except Exception as ex:
            return JsonResponse({"statuscode": "401"})
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
            print(telphone)
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            uid = models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
            data = json.loads(request.body, encoding='utf-8')
            print(data['linkname'])
            user = {
                "initiator_id":uid,
                "travelstartplace":data['travelstartplace'],
                "travelstrattime":data['travelstrattime'],
                "travelendtime":data['travelendtime'],
                "menbers":data['menbers'],
                "linkname":data['linkname'],
                "linknumber":data['linknumber'],
                "destribe":data['destribe'],
                "pubtime":datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            print(user)
            try:
                uu = models.UserAriseTravel.objects.create(**user)
                return JsonResponse({"statuscode": "201"})
            except Exception as ex:
                return JsonResponse({"statuscode": "401"})
        else:
            return JsonResponse({"statuscode": "402"})

# 查询所有活动
def queryAllTravel(request):
    if request.method == 'POST':
        try:
            travels=models.UserAriseTravel.objects.all().values()
            travels=list(travels)

            return JsonResponse(travels,safe=False)
        except Exception as ex:
            return JsonResponse({"statuscode": "401"})
    else:
        return JsonResponse({"statuscode": "402"})
# 用户根据活动id参与活动
def joinTravelByid(request):
# 测试数据:
    # data = {
    #     "joiner_id": "46",
    #     "joinTravel_id": "2",
    # }
    if request.method == 'POST':
        try:
            uu=json.loads(request.body)
            data={
                "joiner_id":uu['joiner_id'],
                "joinTravel_id":uu['joinTravel_id'],
                "jointime":datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            res=models.UserJoinTravel.objects.create(**data)
            return JsonResponse({"statuscode": "808"})
        except Exception as ex:
            print(ex)
            return JsonResponse({"statuscode": "401"})
    else:
        return JsonResponse({"statuscode": "402"})
