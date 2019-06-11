from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .filters import GoodsFilter, CategoriesFilter
from .models import Goods, GoodsCategory, Banner
from .serializers import GoodsSerializer, CategorySerializer1, BannerSerializer, IndexCategorySerializer


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_description = "分页，每页显示数据数量"
    page_size_query_param = 'page_size0'
    page_query_param = "page"
    max_page_size = 100


class GoodsListViewset(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页， 分页/搜索/过滤/排序
    """
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = Goods.objects.all()
    queryset = Goods.objects.all().order_by('-id')
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        from rest_framework.response import Response
        return Response(serializer.data)


# 商品分类接口
class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list：商品分类列表
    retrieve:获取商品分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer1
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CategoriesFilter


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图
    """
    serializer_class = BannerSerializer
    queryset = Banner.objects.all().order_by('index')


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    serializer_class = IndexCategorySerializer
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=['生鲜食品', '精品肉类', '酒水饮料'])
