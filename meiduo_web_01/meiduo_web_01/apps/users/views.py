from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import CreateUserSerializer
from .models import User
from . import serializers


class EmailView(UpdateAPIView):
    '''添加邮箱 更新邮箱'''
    # 权限设置，需要登录客户才能返回数据
    permission_classes = (IsAuthenticated,)

    serializer_class = serializers.EmailSerializer

    def get_object(self):
        '''这个方法中返回当前的登录用户的user信息,因为前端没有传入pk主
        键到视图中所以需要重写RetrieveAPIView的get_object()'''
        return self.request.user

# 根据前端的token进行状态保持的个人中心 返回单一对象
class UserDetailView(RetrieveAPIView):
    '''用户基本信息的获取
    权限设置，需要登录客户才能返回数据
    '''
    permission_classes = (IsAuthenticated,)
    # 指定序列化器
    serializer_class = serializers.UserDetailSerializer

    def get_object(self):
        '''这个方法中返回当前的登录用户的user信息,因为前端没有传入pk主
        键到视图中所以需要重写RetrieveAPIView的get_object()'''
        return self.request.user

# 第五个接口注册的视图
class UserView(CreateAPIView):
    '''注册'''
    # 新增
    serializer_class = CreateUserSerializer


# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
class MobileCountView(APIView):
    """
    手机号数量
    """
    def get(self, request, mobile):
        """
        获取指定手机号数量
        """
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)


# 第三个接口，判断用户名是否存在
# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
class UsernameCountView(APIView):
    """
    用户名数量
    """
    def get(self, request, username):
        """
        获取指定用户名数量
        """
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }

        return Response(data)






