from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,response

from django.db.models import Min,Avg,Max,Sum,Count
from utils.tokenHelper import *
from . import models
import json
# Create your views here.
# 根据用户id查询用户编写的文章
def queryWritebyuid(request):
    if request.method == 'POST':
        # try:
            token=request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone=jwtDecoding(token)['some']
                uid=models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
                data=models.Aritical.objects.filter(yonghu__id=uid).values('id','content','type__typename','pubtime')
                for i in range(len(data)):
                    data[i]["pubtime"]=datetime.datetime.strftime(data[i]["pubtime"],'%Y-%m-%d %H:%M:%S')
                    data[i]['starnum']=len(models.ArticalStart.objects.filter(artical__id=data[i]['id']).annotate(Count('id')).values('id'))
                    data[i]['commennum']=len(models.ArticalComment.objects.filter(artical__id=data[i]['id']).annotate(Count('id')).values('id'))
                print(str(list(data)))
                if data:
                    return JsonResponse(list(data),safe=False)
                else:
                    return JsonResponse({"code": "408"})
            else:
                return JsonResponse({"code": "408"})
    #     except Exception as ex:
    #         return JsonResponse({"code": "408"})
    # else:
    #     return JsonResponse({"code": "408"})

# 查询所有文章
def queryAllAritical(request):
    if request.method == 'POST':
        # try:

                data=models.Aritical.objects.all().values('id','content','type__typename','pubtime','yonghu__uname')
                for i in range(len(data)):
                    data[i]["pubtime"]=datetime.datetime.strftime(data[i]["pubtime"],'%Y-%m-%d %H:%M:%S')
                    data[i]['starnum']=len(models.ArticalStart.objects.filter(artical__id=data[i]['id']).annotate(Count('id')).values('id'))
                    data[i]['commennum']=len(models.ArticalComment.objects.filter(artical__id=data[i]['id']).annotate(Count('id')).values('id'))
                print(str(list(data)))
                if data:
                    return JsonResponse(list(data),safe=False)
                else:
                    return JsonResponse({"code": "408"})

    #     except Exception as ex:
    #         return JsonResponse({"code": "408"})
    # else:
    #     return JsonResponse({"code": "408"})
# 根据用户id查询用户点赞过的文章
def queryLikebyuid(request):
    if request.method == 'POST':
        try:
            token=request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone=jwtDecoding(token)['some']
                uid=models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
                data=models.ArticalStart.objects.filter(liker__id=uid).values('artical__id','artical__content','pubtime','liker__uname')
                for i in range(len(data)):
                    data[i]["pubtime"]=datetime.datetime.strftime(data[i]["pubtime"],'%Y-%m-%d %H:%M:%S')
                    data[i]['starnum']=len(models.ArticalStart.objects.filter(artical__id=1).values('id'))
                    data[i]['commennum']=len(models.ArticalComment.objects.filter(artical__id=data[i]['artical__id']).values('id'))
                print(str(list(data)))
                if data:
                    return JsonResponse(list(data),safe=False)
                else:
                    return JsonResponse({"code": "408"})
            else:
                return JsonResponse({"code": "408"})
        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 根据用户id查询用户评论过的文章
def queryCommentbyuid(request):
    if request.method == 'POST':
        # try:
            token=request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone=jwtDecoding(token)['some']
                uid=models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
                data=models.ArticalComment.objects.filter(commener__id=uid).values('artical__id','artical__content','pubtime','commener__uname')
                for i in range(len(data)):
                    data[i]["pubtime"]=datetime.datetime.strftime(data[i]["pubtime"],'%Y-%m-%d %H:%M:%S')
                    data[i]['starnum'] = len(models.ArticalStart.objects.filter(artical__id=1).values('id'))
                    data[i]['commennum'] = len(models.ArticalComment.objects.filter(artical__id=data[i]['artical__id']).values('id'))
                print(str(list(data)))
                if data:
                    return JsonResponse(list(data),safe=False)
                else:
                    return JsonResponse({"code": "408"})
            else:
                return JsonResponse({"code": "408"})
    #     except Exception as ex:
    #         return JsonResponse({"code": "408"})
    # else:
    #     return JsonResponse({"code": "408"})

# 根据文章id查询评论人
def queryCommentbyaid(request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body,encoding='utf-8')
            aid=data['aid']
            data=models.ArticalComment.objects.filter(artical__id=aid).values('content','pubtime','commener__uname')
            for item in data:
                item["pubtime"]=datetime.datetime.strftime(item["pubtime"],'%Y-%m-%d %H:%M:%S')
            print(str(list(data)))
            if data:
                return JsonResponse(list(data),safe=False)
            else:
                return JsonResponse({"code": "408"})

        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 根据文章id查询点赞人
def queryLikebyaid(request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body,encoding='utf-8')
            aid=data['aid']
            data=models.ArticalStart.objects.filter(artical__id=aid).values('pubtime','liker__uname')
            for item in data:
                item["pubtime"]=datetime.datetime.strftime(item["pubtime"],'%Y-%m-%d %H:%M:%S')
            print(str(list(data)))
            if data:
                return JsonResponse(list(data),safe=False)
            else:
                return JsonResponse({"code": "408"})

        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 添加文章
def addAritical(request):
    if request.method == 'POST':
        try:
            token=request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone=jwtDecoding(token)['some']
                data=json.loads(request.body,encoding='utf-8')
                article={
                    "content":data["content"],
                    "type_id":models.AriticalType.objects.filter(typename=data['ariticaltype']).values('id')[0]['id'],
                    "yonghu_id":models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']
                }
                flag=models.Aritical.objects.create(**article)
                if flag:
                    return JsonResponse({"code": "208"})
                else:
                    return JsonResponse({"code": "408"})
            else:
                return JsonResponse({"code": "408"})
        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 根据文章id添加评论
def addComment(request):
    if request.method == 'POST':
        try:
            token=request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone=jwtDecoding(token)['some']
                data=json.loads(request.body,encoding='utf-8')
                comment={
                    "content":data["content"],
                    "commener_id":models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id'],
                    "artical_id":data["aid"]
                }
                flag=models.ArticalComment.objects.create(**comment)
                if flag:
                    return JsonResponse({"code": "208"})
                else:
                    return JsonResponse({"code": "408"})
            else:
                return JsonResponse({"code": "408"})
        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 根据文章id点赞
def addLike(request):
    if request.method == 'POST':
        try:
            token=request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone=jwtDecoding(token)['some']
                data=json.loads(request.body,encoding='utf-8')
                star={
                    "liker_id":models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id'],
                    "artical_id":data["aid"]
                }
                flag=models.ArticalStart.objects.create(**star)
                if flag:
                    return JsonResponse({"code": "208"})
                else:
                    return JsonResponse({"code": "408"})
            else:
                return JsonResponse({"code": "408"})
        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 根据文章id取消点赞
def deletelike(request):
    pass