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
from django.views.static import serve
from django.conf import settings
#主路由
urlpatterns = [
    url(r'admin/', admin.site.urls),
    # 匹配空路由
    url(r'^$', views.index,name='myindex'),
    #路由部分
    url(r'^user/', include('user.urls',namespace='car_django.user')),
    url(r'^car/', include('car.urls',namespace='car_django.car')),
    url(r'^travel/', include('traval.urls',namespace='car_django.traval')),
    url(r'^boke/', include('boke.urls',namespace='car_django.boke')),
    url(r'media/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT})
]