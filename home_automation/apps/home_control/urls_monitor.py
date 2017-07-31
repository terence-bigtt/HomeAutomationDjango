from django.conf.urls import url

from . import views_monitor

urlpatterns = [
    url(r'^$', views_monitor.monitor, name='index'),
    url(r'^(?P<cam_id>\w+)$', views_monitor.monitor),
    url(r'^(?P<cam_id>\w+)/feed$', views_monitor.feed, name='feed'),
    url(r'^(?P<cam_id>\w+)/preview$', views_monitor.preview, name='preview'),
    url(r'^(?P<cam_id>\w+)/command/(?P<ctrl>\w+)$', views_monitor.cam_ctrl, name='command'),
    url(r'^links$', views_monitor.links, name='links')
]
