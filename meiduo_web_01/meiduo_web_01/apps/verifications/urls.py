# from meiduo_web_01.meiduo_web_01.apps.verifications import views
from . import views

from django.conf.urls import url
urlpatterns = [
    url(r'image_code/(?P<image_code_id>[\w-]+)/^$', views.ImageCodeView.as_view()),
]

