from django.conf.urls import url, include
from django.urls import reverse_lazy
from .views_common import LoginView, index, logout, change_password

urlpatterns = [
    url(r'^profile/login$', LoginView.as_view(), name='login'),
    url(r'^profile/logout$', logout, name='logout'),
    url(r'^profile/change_password', change_password, name = 'change_password'),
    url(r'^$', index, name='index')
]
