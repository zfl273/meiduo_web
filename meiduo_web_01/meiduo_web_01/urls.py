"""meiduo_web_01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # ckeditor路由
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # 添加apps里的verifications
    url(r'^', include('verifications.urls')),

    # 添加users的url
    url(r'^', include('users.urls')),

    # 添加oauth的url
    url(r'^oauth/', include('oauth.urls')),

    # Areas省市区
    url(r'^', include('areas.urls')),

    #
    # url(r'^', include('goods.urls')),


]
