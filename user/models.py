from django.db import models
from car.models import CityStore,CarBase
import json
# Create your models here.
# 用户头像
class UserIcon(models.Model):
    iconurl=models.CharField(max_length=30)

# 用户基本信息
class UserBase(models.Model):
    uname=models.CharField(unique=True,max_length=30)
    telephone=models.CharField(unique=True,max_length=30)
    password=models.CharField(max_length=100)
    icon=models.ForeignKey(to='UserIcon',to_field='id',on_delete=models.CASCADE,default=1)
    pub_time=models.DateTimeField(auto_now_add=True)
    email=models.CharField(max_length=50,null=True)
    # 新建外键约束
    # 外键约束的名称:leixing_id
    # leixing=models.ForeignKey(to='Type',to_field='id',on_delete=models.CASCADE,default=1)

    def __str__(self):
        user={}
        user['telephone']=self.telephone
        user['password']=self.password
        # user['pub_time']=self.pub_time.strftime()
        return json.dumps(user)

# 用户详细信息
class UserDetail(models.Model):
    realname=models.CharField(max_length=100)
    idcard=models.CharField(max_length=100)
    idcardtime=models.DateTimeField()
    address=models.CharField(max_length=100)
    urgentname=models.CharField(max_length=30)
    urgenttel=models.CharField(unique=True,max_length=30)
    add_time=models.DateTimeField(auto_now_add=True)
    yonghu=models.ForeignKey(to='UserBase',to_field='id',on_delete=models.CASCADE)

# # 类型表为主表
# class Type(models.Model):
#     name=models.CharField(unique=True,max_length=50)
# 订单状态表
class OrderState(models.Model):
    statename=models.CharField(max_length=20)
# 订单类型表
class OrderType(models.Model):
    typename = models.CharField(max_length=20)
# 还车表
class ReturnCar(models.Model):
    returncar = models.ForeignKey(to=CityStore, to_field='id', on_delete=models.CASCADE)
# 用户订单表
class UserOrder(models.Model):
    yonghu = models.ForeignKey(to=UserBase, to_field='id', on_delete=models.CASCADE)
    car=models.ForeignKey(to=CarBase,to_field='id',on_delete=models.CASCADE)
    takecarplace=models.ForeignKey(to=CityStore,to_field='id',on_delete=models.CASCADE)
    takecartime=models.DateTimeField()
    returncarplace=models.ForeignKey(to=ReturnCar,to_field='id',on_delete=models.CASCADE)
    returncartime=models.DateTimeField()
    add_time=models.DateTimeField(auto_now_add=True)
    orderstate=models.ForeignKey(to=OrderState,to_field='id',on_delete=models.CASCADE,default=1)
    ordertype=models.ForeignKey(to=OrderType,to_field='id',on_delete=models.CASCADE,default=1)



