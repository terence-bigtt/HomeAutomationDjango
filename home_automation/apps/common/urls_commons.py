from django.conf.urls import url

from .views_common import LoginView, index

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), 'login'),
    url(r'^index$', index, name='index')
]
