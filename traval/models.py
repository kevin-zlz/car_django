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
    travelstartplace=models.CharField(max_length=50,null=True)
    travelstrattime=models.DateTimeField()
    travelendtime=models.DateTimeField()
    menbers=models.IntegerField()
    linkname=models.CharField(max_length=30)
    linknumber=models.CharField(max_length=30)
    destribe=models.CharField(max_length=100)
    pubtime=models.DateTimeField(default=datetime.now())

# 旅游路线表
class TravelPlace(models.Model):
    places = models.ForeignKey(to=UserAriseTravel, to_field='id', on_delete=models.CASCADE, default=1)

# 旅游参与表
class UserJoinTravel(models.Model):
    # 参与人
    joiner=models.ForeignKey(to=UserBase,to_field='id',on_delete=models.CASCADE,null=True)
    # 参与活动
    joinTravel=models.ForeignKey(to=UserAriseTravel,to_field='id',on_delete=models.CASCADE,null=True)
    # 参与时间
    jointime=models.DateTimeField(auto_now_add=True)