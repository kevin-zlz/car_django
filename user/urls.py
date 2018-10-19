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
from django.conf.urls import url,include
from . import views
app_name = 'user'
#user子路由
urlpatterns = [
    url(r'^$',views.personal,name='personal'),
    # 后面的/不能省略
    url(r'login/', views.login, name='login'),
    url(r'regist/', views.regist, name='regist'),
    url(r'addReturnCar/', views.addReturnCar, name='addReturnCar'),
    url(r'DicLoad/', views.DicLoad, name='DicLoad'),
    url(r'uphead/', views.UpHead, name='UpHead'),
    url(r'addorder/', views.addorder, name='addorder'),
    url(r'queryOrder/', views.queryOrder, name='queryOrder'),
    url(r'^getuser\w*/(?P<id>\d*)', views.getuserbyid, name='getuser'),

]