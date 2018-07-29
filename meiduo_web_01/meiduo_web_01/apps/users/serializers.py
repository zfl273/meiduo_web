import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import User
from celery_tasks.email.tasks import send_verify_email


class EmailSerializer(serializers.ModelSerializer):
    '''更新邮箱'''

    class Meta:
        model = User
        fields = ['id', 'email']
        extra_kwargs = {
            'email': {
                'required': True
            }
        }

    def update(self, instance, validated_data):
        '''重写序列化器的更新数据方法
        1 用于更新某些字段，put是全字段更新
        2 在次发送邮件
        3 user传入的模型对象 instance
        '''
        instance.email = validated_data.get('email')
        instance.save()

        # 生成激活连接 , 生成的方法写在模型类里面，方便调用用户id
        verify_url = instance.generate_verify_email_url()

        # 在保存之后，返回数据之前发送邮件
        send_verify_email.delay(instance.email, verify_url)

        return instance


# 获取单一数据 用户信息的序列化器
class UserDetailSerializer(serializers.ModelSerializer):
    '''获取单一数据 用户信息的序列化器'''
    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'email', 'email_active']


class CreateUserSerializer(serializers.ModelSerializer):
    '''注册的校验序列化器'''

    # 定义模型类属性以外的字段
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)
    token = serializers.CharField(label='登录状态token', read_only=True)  # 增加token字段

    class Meta:
        model = User
        # 输出用的 做序列化'id', 'username', 'mobile'
        # id 是read——only
        # username mobile是write_only
        # 输入的是'password', 'password2', 'sms_code', 'allow 做反序列化
        fields = ['id', 'username', 'mobile', 'password', 'password2', 'sms_code', 'allow', 'token']
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages':{
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    # 追加字段的校验逻辑 mobile
    def validate_mobile(self, value):
        '''验证手机号'''
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号码格式错误')
        return value

    def validate_allow(self, value):
        '''校验用户是否同意协议'''
        if value != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validate(self, data):
        '''判断两次密码'''
        if data['password'] != data['password2']:
            raise serializers.ValidationError('密码不一致')

        # 判断短信验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = data['mobile']
        real_sms_code = redis_conn.get('sms_%s'% mobile)
        if real_sms_code is None:
            raise serializers.ValidationError('无效的短信验证码')
        if data['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误')
        return data

    def create(self, validated_data):
        """
        创建用户
        """
        # 移除数据库模型类中不存在的属性
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']
        user = super().create(validated_data)

        # 调用django的认证系统加密密码
        user.set_password(validated_data['password'])
        user.save()

        # 保存注册数据之后，响应注册结果之前
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER # 生成载he
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # user对象是当前的注册用户对象
        payload = jwt_payload_handler(user)  # 将user加入载体
        token = jwt_encode_handler(payload)  #

        # 将token一并响应出去
        user.token = token

        return user