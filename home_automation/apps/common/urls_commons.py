from django.conf.urls import url

from . import views_common

urlpatterns = [
    url(r'^index$', views_common.index, name='index'),
    ]