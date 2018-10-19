from django.db import models

# Create your models here.
from django.db import models
from user.models import UserBase
import json
# Create your models here.
from datetime import datetime

# 旅游发起表
class UserAriseTravel(models.Model):
    # 发起人
    initiator=models.ForeignKey(to=UserBase,to_field='id',on_delete=models.CASCADE,default=1)
    # 出发地点
    travelstartplace=models.CharField(max_length=50,null=True)
    # 出发时间
    travelstrattime=models.DateTimeField()
    # 活动结束时间
    travelendtime=models.DateTimeField()
    # 成员数
    menbers=models.IntegerField()
    # 联系人
    linkname=models.CharField(max_length=30)
    # 联系电话
    linknumber=models.CharField(max_length=30)
    # 其他描述
    destribe=models.CharField(max_length=100)
    # 发布时间
    pubtime=models.DateTimeField(default=datetime.now())

# 旅游路线表
class TravelPlace(models.Model):
    places = models.ForeignKey(to=UserAriseTravel, to_field='id', on_delete=models.CASCADE, default=1)
    address= models.CharField(max_length=50,default='')


# 旅游参与表
class UserJoinTravel(models.Model):
    # 参与人
    joiner=models.ForeignKey(to=UserBase,to_field='id',on_delete=models.CASCADE,null=True)
    # 参与活动
    joinTravel=models.ForeignKey(to=UserAriseTravel,to_field='id',on_delete=models.CASCADE,null=True)
    # 参与时间
    jointime=models.DateTimeField(auto_now_add=True)