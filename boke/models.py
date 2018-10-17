from django.db import models
from user.models import UserBase
# Create your models here.
from django.db import models


class AriticalType(models.Model):
    # 类型名称
    typename=models.CharField(max_length=50)
#
# class ArticalComment(models.Model):
#     pass

class Aritical(models.Model):
    yonghu=models.ForeignKey(to=UserBase,to_field='id',on_delete=models.CASCADE,default=1)
    # 内容
    content=models.TextField(max_length=500)
    # 发表时间
    pubtime=models.DateTimeField(auto_now_add=True)
    # 文章标签
    type=models.ForeignKey(to=AriticalType,to_field='id',on_delete=models.CASCADE,default=1)

class ArticalComment(models.Model):
    # 文章
    artical=models.ForeignKey(to=Aritical,to_field='id',on_delete=models.CASCADE,default=1)
    # 评论人
    commener=models.ForeignKey(to=UserBase,to_field='id',on_delete=models.CASCADE,default=1)
    # 评论内容
    content=models.TextField(max_length=500,default='')
    # 评论时间
    pubtime = models.DateTimeField(auto_now_add=True)


class ArticalStart(models.Model):
    # 文章
    artical = models.ForeignKey(to=Aritical, to_field='id', on_delete=models.CASCADE, default=1)
    # 评论人
    liker = models.ForeignKey(to=UserBase, to_field='id', on_delete=models.CASCADE, default=1)
    # 评论时间
    pubtime = models.DateTimeField(auto_now_add=True)
