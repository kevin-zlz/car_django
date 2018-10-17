from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,response
import json
# Create your views here.
# 根据用户id查询用户编写的文章
def queryWritebyuid(request):
    pass

# 根据用户id查询用户点赞过的文章
def queryLikebyuid(request):
    pass

# 根据用户id查询用户评论过的文章
def queryCommentbyuid(request):
    pass

# 根据文章id查询评论人
def queryCommentbyaid(request):
    pass

# 根据文章id查询点赞人
def queryLikebyaid(request):
    pass

# 添加文章
def addAritical(request):
    pass

# 根据文章id添加评论
def addComment(request):
    pass

# 根据文章id点赞
def addLike(request):
    pass

# 根据文章id取消点赞
def deletelike(request):
    pass