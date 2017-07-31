from .models import MenuItem


def global_settings(request=None):
    menu = MenuItem.objects.order_by('id')
    return {"MENU": menu}
