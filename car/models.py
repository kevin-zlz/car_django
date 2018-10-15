from django.db import models

# Create your models here.
from django.db import models
import json
# Create your models here.
class City(models.Model):
    cityname=models.CharField(max_length=30)
    strictname=models.CharField(max_length=50)

class CityStore(models.Model):
    storename=models.CharField(max_length=50)
    storeaddress=models.ForeignKey(to='City',to_field='id',on_delete=models.CASCADE,default=1)
    detailaddress=models.CharField(max_length=100)
    storetel=models.CharField(max_length=30)
    storetime=models.CharField(max_length=50)

class CarBase(models.Model):
    storeid=models.ForeignKey(to='CityStore',to_field='id',on_delete=models.CASCADE,default=1)
    carid=models.CharField(max_length=30)
    carname=models.CharField(max_length=30)
    price=models.IntegerField()
    brand=models.CharField(max_length=100)
    cartype=models.CharField(max_length=30)

class CarImages(models.Model):
    car = models.ForeignKey(to='CarBase', to_field='id', on_delete=models.CASCADE, default=1)
    icon = models.CharField(max_length=100, default='user.jpg')
    # 新建外键约束
    # 外键约束的名称:leixing_id
    # leixing=models.ForeignKey(to='Type',to_field='id',on_delete=models.CASCADE,default=1)

class CarDetail(models.Model):
    car=models.ForeignKey(to='CarBase',to_field='id',on_delete=models.CASCADE,default=1)
    # 车系
    chexi=models.CharField(max_length=30)
    # 年代款
    niandaikuan=models.CharField(max_length=30)
    # 配置款
    peizhikun=models.CharField(max_length=30)
    # 座位数
    sitenum=models.CharField(max_length=100)
    # 车门数
    doornum=models.CharField(max_length=30)
    # 燃油类型
    oiltype=models.CharField(max_length=30)
    # 变速箱类型
    changespeed=models.CharField(max_length=30)
    # 排量
    pailiang=models.CharField(max_length=30)
    # 燃油标号
    oilnum=models.CharField(max_length=30)
    # 驱动
    qudong=models.CharField(max_length=30)
    # 油箱容量
    oilcaptiy=models.CharField(max_length=30)
    # 车窗
    carwindow=models.CharField(max_length=30)
    # 座椅类型
    sitetype=models.CharField(max_length=30)
    # 音箱
    musicnum = models.CharField(max_length=30)
    # 气囊
    isqinang=models.CharField(max_length=30)
    # 倒车雷达
    isdaocheleida=models.CharField(max_length=30)
    # GPS
    isgps=models.CharField(max_length=30)
    # DVD
    isdvd=models.CharField(max_length=30)
    # 进气形式
    jinqixingshi=models.CharField(max_length=30)



