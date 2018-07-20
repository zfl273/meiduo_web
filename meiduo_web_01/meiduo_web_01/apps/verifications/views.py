from django.shortcuts import render
from django.http import HttpResponse
# from rest_framework.generics import GenericAPIView
from rest_framework.generics import GenericAPIView

from meiduo_web_01.libs.captcha.captcha import captcha
from django_redis import get_redis_connection # 获取redis连接对象
from . import constants
from rest_framework.views import APIView
from . import serializers
from meiduo_web_01.libs.yuntongxun.sms import CCP
from celery_tasks.sms.tasks import send_sms_code

import random
from rest_framework.response import Response
# 创建一个日志输出器
import logging
# 记录日志
logger = logging.getLogger('django')

# Create your views here.


class ImageCodeView(APIView):
    '''
    图片验证码
    # url(r'^image_codes/(?P<image_code_id>[\w-]+)/$', views.ImageCodeView.as_view()),

    '''
    def get(self, request,image_code_id):
        # 生成图片验证码的内容和图片
        text, image = captcha.generate_captcha()
        logger.info('图片验证码:%s'% text)# 打印图片验证码
        # 将图片验证码的内容存储到redis数据库的2号库
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.set('img_%s'% image_code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
        # 将图片响应给用户
        return HttpResponse(image, content_type='image/jpg')


# 访问方式： GET /sms_codes/(?P<mobile>1[3-9]\d{9})/?image_code_id=xxx&text=xxx
class SMSCodeView(GenericAPIView): # 可以是APIview 或者 View
    '''
    get 发送短信验证码视图
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view())
    '''
    # 指定序列化器
    serializer_class = serializers.ImageCodeCheckSerializer

    def get(self, request, mobile):
        # 接受参数：mobile， image_code_id,  text
        # 校验参数：image_code_id, text
        # 对比text和服务器存储的图片验证内容（genericAPIView放在序列化器里做，不需要模型）

        # 创建序列化器对象
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # 生成随机短信验证码,6位
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info('短信验证码：%s' % sms_code) # 短信验证码
        # 发送短信验证码ccp.send_template_sms('18949599846', ['1234', 5], 1)
        # CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRED//60], 1)
        # 异步发送短信需要:delay->将延时任务添加到队列并触发异步任务
        # 如果不调用delay任务也能完成，只是不会info打印出来
        send_sms_code.delay(mobile, sms_code)

        # 存储短信验证d码
        redis_conn = get_redis_connection('verify_codes')
        # redis_conn.set('key', 'value', 'time')
        # redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRED, sms_code)
        # redis_conn.setex('send_flag_%s'%mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 优化访问数据库，使用redis管道,两次操作一次访问就足够
        pl = redis_conn.pipeline()
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRED, sms_code)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 放入管道 ，需要执行
        pl.execute()
        # 响应发送短信验证结果
        return Response({'message': 'OK'})
