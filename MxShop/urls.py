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
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

import xadmin
from goods.views import GoodsListViewSet, CategoryViewSet
from useroperation.views import UserFavViewSet, LeavingMessageViewset, AddressViewset
from users.views import RegSmsCodeViewSet, UserViewSet
from trade.views import ShoppingCartViewSet
from .settings import MEDIA_ROOT

goods_list = GoodsListViewSet.as_view({
    'get': 'list',
})

router = DefaultRouter()
router.register('goods', GoodsListViewSet, basename='goods')  # 配置goods的url
router.register('categories', CategoryViewSet, base_name="categories")  # 配置category的url
router.register('code', RegSmsCodeViewSet, basename='code')  # 配置验证码的url
router.register('users', UserViewSet, basename='users')  # 用户注册的url
router.register('userfavs', UserFavViewSet, basename='userfavs')  # 用户收藏url
router.register('messages', LeavingMessageViewset, basename='messages')  # 用户留言url
router.register('address', AddressViewset, basename='address')  # 用户收货地址url
router.register('shopcarts', ShoppingCartViewSet, basename='shopcarts')  # 购物车url

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('login/', obtain_jwt_token),
    path('api-auth/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_frameword')),
    path('docs/', include_docs_urls(title='MxShop|DOCS')),

    path('', include(router.urls)),

    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
]
