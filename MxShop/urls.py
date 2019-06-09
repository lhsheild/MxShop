"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.views.static import serve
from django.views.generic import TemplateView
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from goods.views import GoodsListViewset, CategoryViewset
from useroperation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from users.views import RegSmsCodeViewset, UserViewset
from trade.views import ShoppingCartViewset, OrderViewset, AlipayView
from .settings import MEDIA_ROOT

goods_list = GoodsListViewset.as_view({
    'get': 'list',
})

router = DefaultRouter()
router.register('goods', GoodsListViewset, basename='goods')  # 配置goods的url
router.register('categories', CategoryViewset, base_name="categories")  # 配置category的url
router.register('code', RegSmsCodeViewset, basename='code')  # 配置验证码的url
router.register('users', UserViewset, basename='users')  # 用户注册的url
router.register('userfavs', UserFavViewset, basename='userfavs')  # 用户收藏url
router.register('messages', LeavingMessageViewset, basename='messages')  # 用户留言url
router.register('address', AddressViewset, basename='address')  # 用户收货地址url
router.register('shopcarts', ShoppingCartViewset, basename='shopcarts')  # 购物车url
router.register('orders', OrderViewset, basename='orders')  # 订单url

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('login/', obtain_jwt_token),
    path('api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_frameword')),
    path('docs/', include_docs_urls(title='MxShop|DOCS')),

    path('alipay/return/', AlipayView.as_view(), name='alipay'),
    path('index/', TemplateView.as_view(template_name='index.html'), name='index'),

    path('', include(router.urls)),

    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
]
