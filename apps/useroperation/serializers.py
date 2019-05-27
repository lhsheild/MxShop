from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from goods.serializers import GoodsSerializer
from .models import UserFav, UserLeavingMessage, UserAddress

User = get_user_model()


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ('goods', 'id')


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message='已经收藏'
            )
        ]
        fields = ('user', 'goods', 'id')


class UserLeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserLeavingMessage
        fields = ('user', 'message_type', 'subject', 'message', 'file', 'id', 'add_time')


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = UserAddress
        fields = ('user', 'province', 'city', 'district', 'address', 'signer_name', 'signer_mobile', 'id', 'add_time')

    def validate_province(self, province):
        if not province:
            raise serializers.ValidationError('省份不能为空！')
        print('province', province, type(province))
        return province

    def validate_city(self, city):
        if not city:
            raise serializers.ValidationError('城市不能为空！')
        print('city', type(city))
        return city

    def validate_signer_name(self, signer_name):
        if not signer_name:
            raise serializers.ValidationError('签收人不能为空！')
        return signer_name

    def validate_signer_mobile(self, signer_mobile):
        if not signer_mobile:
            raise serializers.ValidationError('联系电话不能为空！')
        return signer_mobile

    def validate(self, attrs):
        if not attrs.get('province'):
            raise serializers.ValidationError('省份不能为空！')
        elif not attrs.get('city'):
            raise serializers.ValidationError('城市不能为空！')
        elif not attrs.get('signer_name'):
            raise serializers.ValidationError('签收人不能为空！')
        elif not attrs.get('signer_mobile'):
            raise serializers.ValidationError('联系电话不能为空！')
        return attrs
