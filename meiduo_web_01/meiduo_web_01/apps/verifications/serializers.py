from rest_framework import serializers
from django_redis import get_redis_connection


# 定义序列化器，用来验证
class ImageCodeCheckSerializer(serializers.Serializer):
    """
    校验图片验证码的序列化器
    """
    # 拿到校验字段类型 ，定义校验字段:定义的校验字段要么和模型类的属性一样，要么和参数的key一样，这里和key一样
    image_code_id = serializers.UUIDField(format='hex_verbose')
    text = serializers.CharField(max_length=4, min_length=4)
    # serializer不是只能为数据库模型类定义，也可以为非数据库模型类的数据定义。
    # serializer是独立于数据库之外的存在
    def validate(self, attrs):
        '''校验'''

        # 读取validated_data里面的数据
        image_code_id = attrs.get('image_code_id')
        text = attrs.get('text')

        # 获取连接到redis的对象
        redis_conn = get_redis_connection('verify_codes')

        # 获取redis中存储的图片验证码
        image_code_server = redis_conn.get('img_%s' % image_code_id)



