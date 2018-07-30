from rest_framework import serializers

from .models import Area


class AreasSerializer(serializers.ModelSerializer):
    '''list省级数据的序列化，只做序列化'''

    class Meta:
        model = Area
        fields = ['id', 'name']


class SubsAreasSerializer(serializers.ModelSerializer):
    '''retrieve省级数据的序列化器：只做序列化'''

    subs = AreasSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ['id', 'name', 'subs']
