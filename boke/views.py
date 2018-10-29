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
                isover=False
                mydata = json.loads(request.body, encoding='utf-8')
                index=mydata['index']
                pagesize=mydata['pagesize']
                data=models.Aritical.objects.all().order_by('-pubtime').values('id','title','content','type__typename','pubtime','yonghu__uname','yonghu__icon_id__iconurl')
                for i in range(len(data)):
                    data[i]["pubtime"]=datetime.datetime.strftime(data[i]["pubtime"],'%Y-%m-%d %H:%M:%S')
                    data[i]['starnum']=len(models.ArticalStart.objects.filter(artical__id=data[i]['id']).annotate(Count('id')).values('id'))
                    data[i]['commennum']=len(models.ArticalComment.objects.filter(artical__id=data[i]['id']).annotate(Count('id')).values('id'))
                if len(data)>index*pagesize-1:
                    data=data[0:index*pagesize]
                    isover=True
                res={
                    "mydata":list(data),
                    "isover":isover,
                }
                if data:
                    return JsonResponse(res,safe=False)
                else:
                    return JsonResponse({"code": "408"})

    #     except Exception as ex:
    #         return JsonResponse({"code": "408"})
    # else:
    #     return JsonResponse({"code": "408"})



# 根据文章id查询所有文章
def queryAriticalByaid(request):
    if request.method == 'POST':
        # try:
                data = json.loads(request.body, encoding='utf-8')
                aid = data['aid']
                data=models.Aritical.objects.filter(id=aid).values('id','content','type__typename','pubtime','yonghu__uname','yonghu__icon_id__iconurl')
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
                data=models.ArticalStart.objects.filter(liker__id=uid).values('id','artical__id','artical__content','pubtime','liker__uname','artical__yonghu__uname')
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
                data=models.ArticalComment.objects.filter(commener__id=uid).values('id','artical__id','artical__content','pubtime','commener__uname','content','artical__yonghu__uname')
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
            data=models.ArticalComment.objects.filter(artical__id=aid).values('id','content','pubtime','commener__uname','commener__telephone','commener__icon_id__iconurl')
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
            data=models.ArticalStart.objects.filter(artical__id=aid).values('liker__telephone','pubtime','liker__uname')
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
        # try:
            token=request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone=jwtDecoding(token)['some']
                data=json.loads(request.body,encoding='utf-8')
                article={
                    "title":data['title'],
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
        # except Exception as ex:
        #     return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 根据文章id添加评论
def addComment(request):
    if request.method == 'POST':
        # try:
            token=request.META.get('HTTP_TOKEN')
            print(token)
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
    #     except Exception as ex:
    #         return JsonResponse({"code": "408"})
    # else:
    #     return JsonResponse({"code": "408"})

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
    if request.method == 'POST':
        # try:
            token = request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone = jwtDecoding(token)['some']
                data=json.loads(request.body,encoding='utf-8')
                aid=data['aid']
                data=models.ArticalStart.objects.get(artical__id=aid,liker__id=models.UserBase.objects.filter(telephone=telphone).values('id')[0]['id']).delete()
                if data:
                    return JsonResponse({"code":"208"})
                else:
                    return JsonResponse({"code": "408"})

        # except Exception as ex:
        #     return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})


# 根据评论id删除个人评论
def deteleCommentByCid(request):
    if request.method == 'POST':
        try:
            token = request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone = jwtDecoding(token)['some']
                data=json.loads(request.body,encoding='utf-8')
                cid=data['cid']
                print(cid)
                data=models.ArticalComment.objects.get(id=cid).delete()
                if data:
                    return JsonResponse({"code":"208"})
                else:
                    return JsonResponse({"code": "408"})

        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 查询文章所有类型
def queryArticlaType(request):
    if request.method == 'POST':
        try:
                data=models.AriticalType.objects.all().values()
                if data:
                    return JsonResponse(list(data),safe=False)
                else:
                    return JsonResponse({"code": "408"})
        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})


# 删除文章及其评论点赞根据文章id
def deleteArticalByaid(request):
    if request.method == 'POST':
        try:
            token=request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone=jwtDecoding(token)['some']
                data = json.loads(request.body, encoding='utf-8')
                aid = data['aid']
                like= models.ArticalStart.objects.filter(artical__id=aid).delete()
                comment = models.ArticalComment.objects.filter(artical__id=aid).delete()
                art = models.Aritical.objects.filter(id=aid).delete()
                if art:
                    return JsonResponse({"code": "208"})
                else:
                    return JsonResponse({"code": "408"})
        except Exception as ex:
            return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})

# 根据点赞id取消点赞
def deletelikebysid(request):
    if request.method == 'POST':
        # try:
            token = request.META.get('HTTP_TOKEN')
            if jwtDecoding(token):
                telphone = jwtDecoding(token)['some']
                data=json.loads(request.body,encoding='utf-8')
                sid=data['sid']
                data=models.ArticalStart.objects.get(id=sid).delete()
                if data:
                    return JsonResponse({"code":"208"})
                else:
                    return JsonResponse({"code": "408"})

        # except Exception as ex:
        #     return JsonResponse({"code": "408"})
    else:
        return JsonResponse({"code": "408"})