from rest_framework.authentication import SessionAuthentication
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer, UserLeavingMessageSerializer, UserAddressSerializer


# Create your views here.
class UserFavViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """
    list:获取用户收藏李彪
    retrieve:判断某个商品是否已经收藏
    create:收藏商品
    """
    # queryset = UserFav.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # serializer_class = UserFavSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        elif self.action == 'create':
            return UserFavSerializer

        return UserFavSerializer


class LeavingMessageViewset(ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    """
    list:获取用户留言
    create:添加留言
    destroy:删除留言
    """

    serializer_class = UserLeavingMessageSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AddressViewset(ModelViewSet):
    """
    收获地址管理
    list:获取收货地址列表
    create:新建收获地址
    destroy:删除收货地址
    update:更新收货地址
    retrieve:获取详细收获地址
    """

    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
