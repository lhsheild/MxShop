import os

from django.db.models import Q

from utils.email_send import send_register_email

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MxShop.settings")
    import django

    django.setup()

    from goods import models

    value = 40

    # goods = models.Goods.objects.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
    #     category__parent_category__parent_category_id=value))
    # print(len(goods))

    send_register_email('lhsheild@sina.com', code=1234)