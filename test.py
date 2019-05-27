import os

from django.db.models import Q

from utils.email_send import send_register_email

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MxShop.settings")
    import django

    django.setup()

    from users.models import UserProfile

    user = UserProfile.objects.get(username='lhsheild')
    user.set_password('123456')
    user.save()