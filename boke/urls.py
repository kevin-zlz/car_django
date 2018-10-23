"""car_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import views

app_name = 'boke'
#主路由
urlpatterns = [
    # url(r'admin/', admin.site.urls),
    # # 匹配空路由
    # url(r'^$', views.index,name='myindex'),
    # #路由部分
    url(r'queryWritebyuid/', views.queryWritebyuid, name='queryWritebyuid'),
    url(r'queryAllAritical/', views.queryAllAritical, name='queryAllAritical'),
    url(r'queryAriticalByaid/', views.queryAriticalByaid, name='queryAriticalByaid'),
    url(r'queryCommentbyuid/', views.queryCommentbyuid, name='queryCommentbyuid'),
    url(r'queryLikebyuid/', views.queryLikebyuid, name='queryLikebyuid'),
    url(r'queryLikebyaid/', views.queryLikebyaid, name='queryLikebyaid'),
    url(r'queryCommentbyaid/', views.queryCommentbyaid, name='queryCommentbyaid'),
    url(r'queryArticlaType/', views.queryArticlaType, name='queryArticlaType'),
    url(r'addAritical/', views.addAritical, name='addAritical'),
    url(r'addComment/', views.addComment, name='addComment'),
    url(r'addLike/', views.addLike, name='addLike'),
    url(r'deletelike/', views.deletelike, name='deletelike'),
    url(r'deteleCommentByCid/', views.deteleCommentByCid, name='deteleCommentByCid'),
    url(r'deleteArticalByaid/', views.deleteArticalByaid, name='deleteArticalByaid'),
    url(r'deletelikebysid/', views.deletelikebysid, name='deletelikebysid'),
]