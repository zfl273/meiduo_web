# from meiduo_web_01.meiduo_web_01.apps.verifications import views
from . import views

from django.conf.urls import url
urlpatterns = [
    # 图片验证码路由
    url(r'^image_codes/(?P<image_code_id>[\w-]+)/$', views.ImageCodeView.as_view()),

    # 短信验证码路由
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
]

