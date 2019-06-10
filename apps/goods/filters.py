from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Goods, GoodsCategory


class GoodsFilter(filters.FilterSet):
    pricemin = filters.NumberFilter(field_name="shop_price", lookup_expr='gte', help_text='最低价格')
    pricemax = filters.NumberFilter(field_name="shop_price", lookup_expr='lte', help_text='最高价格')
    name = filters.CharFilter(field_name='name', lookup_expr='contains', help_text='商品名')
    top_category = filters.NumberFilter(method='top_category_filter', help_text='一级分类')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']


class CategoriesFilter(filters.FilterSet):
    class Meta:
        model = GoodsCategory
        fields = "__all__"
