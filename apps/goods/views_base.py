from django.views.generic.base import View

from .models import Goods


class GoodsListView(View):
    def get(self, request):
        goods = Goods.objects.all()[:10]
        from django.http import HttpResponse, JsonResponse
        from django.core.serializers import serialize
        goods = serialize('json', goods)
        import json
        goods = json.loads(goods)
        # return HttpResponse(serialize('json', goods), content_type='application/json')
        return JsonResponse(goods, safe=False)