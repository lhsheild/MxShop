from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .models import ShoppingCart, OrderInfo, OrderGoods
from .serializers import ShopCartSerializer, ShopCartDetailSerializer, OrderSerializer, OrderDetailSerializer


class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    购物车功能
    list:
    获取购物车详情
    create:
    加入购物车
    delete:
    删除购物车中商品
    """

    # serializer_class = ShopCartSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer


class OrderViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    """
    订单管理
    list:订单集列表
    delete:删除订单
    create:创建订单
    """
    # serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    # 动态配置serializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order


from rest_framework.views import APIView
from utils.alipay import AliPay
from MxShop.settings import private_key_path, ali_key_path
from datetime import datetime


class AlipayView(APIView):
    def get(self, request):
        """
        处理return_url返回
        :param request:
        :return:
        """
        processed_dict = {}
        for k, v in request.GET.items():
            processed_dict[k] = v

        sign = processed_dict.pop('sign', None)

        alipay = AliPay(
            appid='2016092800616929',
            app_notify_url='http://113.16.255.12:11032/alipay/return',
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_key_path,
            debug=True,
            return_url='http://113.16.255.12:11032/alipay/return'
        )

        verify_re = alipay.verify(processed_dict, sign)
        print('get_dict', processed_dict)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            from django.shortcuts import redirect
            response = redirect('index')
            response.set_cookie('nextPath', 'pay', max_age=2)
            return response
        else:
            from django.shortcuts import redirect
            response = redirect('index')
            return response

    def post(self, request):
        """
        处理notify_url返回
        :param request:
        :return:
        """
        processed_dict = {}
        for k, v in request.POST.items():
            processed_dict[k] = v

        sign = processed_dict.pop('sign', None)

        alipay = AliPay(
            appid='2016092800616929',
            app_notify_url='http://113.16.255.12:11032/alipay/return',
            app_private_key_path=private_key_path,
            alipay_public_key_path=ali_key_path,
            debug=True,
            return_url='http://113.16.255.12:11032/alipay/return'
        )

        verify_re = alipay.verify(processed_dict, sign)
        print(processed_dict)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)
            print(trade_status)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

                from rest_framework.response import Response
            return Response('success')

