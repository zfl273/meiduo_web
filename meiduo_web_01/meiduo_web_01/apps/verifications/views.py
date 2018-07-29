from django.shortcuts import render
import random
import logging
from django.http import HttpResponse

from rest_framework.generics import GenericAPIView
from meiduo_web_01.libs.captcha.captcha import captcha
from django_redis import get_redis_connection  # 获取redis连接对象
from rest_framework.views import APIView
from rest_framework.response import Response
from meiduo_web_01.libs.yuntongxun.sms import CCP

from . import constants
from . import serializers
from celery_tasks.sms.tasks import send_sms_code


# 创建一个日志输出器# 记录日志
logger = logging.getLogger('django')

# Create your views here.


# 第一个接口设计 图片验证码和图片的接口
class ImageCodeView(APIView):
    '''
    图片验证码
    # url(r'^image_codes/(?P<image_code_id>[\w-]+)/$', views.ImageCodeView.as_view()),

    '''
    def get(self, request, image_code_id):
        # 生成图片验证码的内容和图片
        text, image = captcha.generate_captcha()
        logger.info('图片验证码:%s' % text)  # 打印图片验证码

        # django-redis提供了get_redis_connection的方法，
        # 通过调用get_redis_connection方法传递redis的配置名称可获取到redis的连接对象，
        # 通过redis连接对象可以执行redis命令。
        # 将图片验证码的内容存储到redis数据库的2号库
        redis_conn = get_redis_connection('verify_codes')
        # 图片验证码保存到redis-verify
        redis_conn.set('img_%s' % image_code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
        # 将图片响应给用户
        return HttpResponse(image, content_type='images/jpg')


# 第二个接口设计 发送短信验证码的接口
# 请求方式： GET
# 请求路径： /sms_codes/(?P<mobile>1[3-9]\d{9})/?image_code_id=xxx&text=xxx
# 请求参数： 路径参数与查询字符串参数 1： 手机号mobile 2：图片验证码 3 图片uuid
# 参数	         类型	      是否必须	    说明
# mobile	     str	       是	         手机号
# image_code_id	uuid 字符串	   是	         图片验证码编号
# text	         str	       是	         用户输入的图片验证码
# 返回数据：json格式 message	str	否	OK，发送成功
class SMSCodeView(GenericAPIView):
    '''
    get 发送短信验证码视图
    /sms_codes/(?P<mobile>1[3-9]\d{9})/?image_code_id=xxx&text=xxx
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view())
    '''
    # 指定序列化器serializer_class 指明视图使用的序列化器
    serializer_class = serializers.ImageCodeCheckSerializer

    def get(self, request, mobile):
        # 将前端发送过来的数据进行校验, mobile符合正则匹配，校验image_code_id是否可以在数据库找到，text是否一致
        # 创建的序列化对象
        # 注意，该方法在提供序列化器对象的时候，
        # 会向序列化器对象的context属性补充三个数据：request当前视图的请求对象、format 当前请求期望返回的数据格式、viewview 当前请求的类视图对象，
        # 这三个数据对象可以在定义序列化器时使用。
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)  # 开始校验 进入序列化器的validate

        # 先不进行校验，实现发短信
        # 生成随机六位数字的数字，不够的以0补
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info('短信验证码是：%s' % sms_code)
        # 调用第三方接口云通讯进行短信发送ccp = CCP() 属于耗时操作，不能阻塞后续业务逻辑，需要异步发送短信
        # ccp.send_template_sms('18949599846', ['1234', 5], 1)对应的参数为（需要发送短信手机，[内容，过期时间分钟]，1号模版加载内容发送）
        # CCP().send_template_sms(mobile, [sms_code, constants.SEND_SMS_CODE_INTERVAL//60], constants.SMS_CODE_TEMP_ID)
        # 异步发送短信码 调用delay，延时任务添加到任务队列去触发异步任务，worker可以观察到
        send_sms_code.delay(mobile, sms_code)

        # 存储短信验证码到redis到verify_code
        redis_conn = get_redis_connection('verify_codes')
        # 优化储存,使用redis管道，几次访问优化成一次执行，一定需要execulte
        pl = redis_conn.pipeline()
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRED, sms_code)
        # 防止客户端每次暴力请求发送短信，设定60秒内不能重复发短信
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        pl.execute()
        # pl.setex()
        return Response({'message': 'OK'})



    # 指定序列化器
    # serializer_class = serializers.ImageCodeCheckSerializer
    #
    # def get(self, request, mobile):
    #     # 接受参数：mobile， image_code_id,  text
    #     # 校验参数：image_code_id, text
    #     # 对比text和服务器存储的图片验证内容（genericAPIView放在序列化器里做，不需要模型）
    #
    #     # 创建序列化器对象
    #     serializer = self.get_serializer(data=request.query_params)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # 生成随机短信验证码,6位
    #     sms_code = '%06d' % random.randint(0, 999999)
    #     logger.info('短信验证码：%s' % sms_code)  # 短信验证码
    #     # 发送短信验证码ccp.send_template_sms('18949599846', ['1234', 5], 1)
    #     # CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRED//60], 1)
    #     # 异步发送短信需要:delay->将延时任务添加到队列并触发异步任务
    #     # 如果不调用delay任务也能完成，只是不会info打印出来
    #     send_sms_code.delay(mobile, sms_code)
    #
    #     # 存储短信验证d码
    #     redis_conn = get_redis_connection('verify_codes')
    #     # redis_conn.set('key', 'value', 'time')
    #     # redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRED, sms_code)
    #     # redis_conn.setex('send_flag_%s'%mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
    #     # 优化访问数据库，使用redis管道,两次操作一次访问就足够
    #     pl = redis_conn.pipeline()
    #     pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRED, sms_code)
    #     pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
    #     # 放入管道 ，需要执行
    #     pl.execute()
    #     # 响应发送短信验证结果
    #     return Response({'message': 'OK'})
