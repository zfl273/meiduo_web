from django_redis import get_redis_connection
from rest_framework import serializers
from .utils import OAuthQQ

from users.models import User
from .models import OAuthQQUser

class QQAuthUserSerializer(serializers.Serializer):

    access_token = serializers.CharField(label='操作凭证')
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$')
    password = serializers.CharField(label='密码', max_length=20, min_length=8)
    sms_code = serializers.CharField(label='短信验证码')

    def validate(self, data):
        access_token = data['access_token']
        openid = OAuthQQ.check_save_user_token(access_token)
        if not openid:
            raise serializers.ValidationError('无效的access_token')
        data['openid'] = openid

        mobile = data['mobile']
        sms_code = data['sms_code']
        redis_conn = get_redis_connection('verify_codes')
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        if real_sms_code.decode() != sms_code:
            raise serializers.ValidationError('短信验证码错误')
        # 如果用户存在。检查用户密码
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            pass
        else:
            password = data['password']
            if not user.check_password(password):
                raise serializers.ValidationError('密码错误')
            data['user'] = user
        return data


    def create(self, validated_data):
        user = validated_data.get('user')
        if not user: # 如果用户不存在
            user = User.objects.create_user(
                username=validated_data['mobile'],
                password=validated_data['password'],
                mobile=validated_data['mobile']
            ) # 调用管理器方法 create_user(username, email=None, password=None, *\extra_fields*)

        # ruguo用户存在；将用户绑定openid
        OAuthQQUser.objects.create(
            openid=validated_data['openid'],
            user=user
        )
        return user


