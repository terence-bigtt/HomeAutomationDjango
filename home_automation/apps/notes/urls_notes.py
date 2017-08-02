from django.conf.urls import url, include
from django.urls import reverse_lazy
from .views_notes import todo_new

urlpatterns = [
    url(r'^todo/new$', todo_new, name='new_todo'),
]
