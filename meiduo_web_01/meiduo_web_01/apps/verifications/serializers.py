import logging

from rest_framework import serializers
from django_redis import get_redis_connection
from redis import RedisError

logger = logging.getLogger('django')


# 定义序列化器，只用来校验参数
class ImageCodeCheckSerializer(serializers.Serializer):
    """
    校验图片验证码的序列化器
    """
    # 拿到校验字段类型
    # 定义校验字段:定义的校验字段要么和模型类的属性一样，要么和参数的key一样，这里和key一样
    image_code_id = serializers.UUIDField(format='hex_verbose')
    text = serializers.CharField(max_length=4, min_length=4)

    def validate(self, attrs):
        # 传过来的参数
        image_code_id = attrs['image_code_id']
        text = attrs['text']
        print('view是：#####%s' % self.context['view'])
        # print('format是：#####$s' % self.context['format'])
        # print('request是：#####%s' % self.context['request'])
        # 获取redis里的真实数据
        redis_conn = get_redis_connection('verify_codes')
        image_code_server = redis_conn.get('img_%s' % image_code_id)
        # 获取完立即删除数据库中的图片验证码,业务逻辑不是必须的不能阻塞主程序
        try:
            redis_conn.delete('img_%s' % image_code_id)
        except RedisError as e:
            logger.error(e)
        # 没有获取到就是过期了
        if image_code_server is None:
            raise serializers.ValidationError('验证码已经过期')
        # redis存储的都是二进制，两个不一致，py3中redis读取出来的都是二进制
        if text.lower() != image_code_server.decode().lower():
            raise serializers.ValidationError('图片验证码输入有误')
        # 序列化器对象需要获取手机号码
        mobile = self.context['view'].kwargs['mobile']
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        # 如果send——flag存在说明60秒时间未过期，属于频繁操作，不予发送短信
        if send_flag:
            raise serializers.ValidationError('频繁发送短信')

        return attrs

    # image_code_id = serializers.UUIDField(format='hex_verbose')
    # text = serializers.CharField(max_length=4, min_length=4)
    # # serializer不是只能为数据库模型类定义，也可以为非数据库模型类的数据定义。
    # # serializer是独立于数据库之外的存在
    #
    # def validate(self, attrs):
    #     '''校验'''
    #
    #     # 读取validated_data里面的数据
    #     image_code_id = attrs.get('image_code_id')
    #     text = attrs.get('text')
    #
    #     # 获取连接到redis的对象
    #     redis_conn = get_redis_connection('verify_codes')
    #     # 获取redis中存储的图片验证码
    #     image_code_server = redis_conn.get('img_%s' % image_code_id)
    #     # 立即删除数据库中的图片验证码,不能阻塞程序
    #     try:
    #         redis_conn.delete('img_%s' % image_code_id)
    #     except RedisError as e:
    #         logger.error(e)
    #
    #     if image_code_server is None:
    #         raise serializers.ValidationError('验证码已经过期')
    #     # image_code_server = image_code_server.decode()
    #     if text.lower() != image_code_server.decode().lower():
    #         raise serializers.ValidationError('图片验证码输入有误')
    #     #60s内获取短信
    #     mobile = self.context['view'].kwargs['mobile']
    #     send_flag = redis_conn.get('send_flag_%s' % mobile)
    #     if send_flag:
    #         raise serializers.ValidationError('频繁发送短信')
    #     return attrs



