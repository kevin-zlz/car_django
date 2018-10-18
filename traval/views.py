from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,JsonResponse,response
from datetime import datetime
import json
from . import models
# 根据用户id查询用户参与的所有活动
def queryTravelByuid(request):
    pass

# 根据用户id查询用户参与的已结束活动（根据活动结束时间查）
def queryJoinedTravel(request):
    pass

# 根据用户id查询用户参与的未进行活动（根据活动开始时间查）
def queryNotJoinTravel(request):
    pass

# 根据用户id及活动id取消用户参与的未进行活动（根据活动开始时间查）
def cancelNotJoinTravel(request):
    pass

# 根据用户id查询用户发起的所有活动
def queryInitatorTravel(request):
    pass


