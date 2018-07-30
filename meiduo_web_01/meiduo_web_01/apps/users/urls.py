from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url
# from .views import UsernameCountView

from . import views
urlpatterns = [
    # 判断用户存在
    url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),

    # 手机号码是否存在
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),

    # 注册
    url(r'^users/$', views.UserView.as_view()),

    # jwt登录 Django REST framework JWT提供了登录签发JWT的视图，可以直接使用
    url(r'^authorizations/$', obtain_jwt_token),

    # 认证 个人中心
    url(r'user/$', views.UserDetailView.as_view()),

    # 添加邮箱
    url(r'^email/$', views.EmailView.as_view()),

    # 验证邮箱视图
    url(r'emails/verification/$', views.VerifyEmailView.as_view()),

]

router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet, base_name='addresses')

urlpatterns += router.urls
# POST /addresses/ 新建  -> create
# PUT /addresses/<pk>/ 修改  -> update
# GET /addresses/  查询  -> list
# DELETE /addresses/<pk>/  删除 -> destroy
# PUT /addresses/<pk>/status/ 设置默认 -> status
# PUT /addresses/<pk>/title/  设置标题 -> title
