from django.conf.urls import url, include
from django.urls import reverse_lazy
from .views_notes import todo_new, preview_todo, index

urlpatterns = [
    url(r'^todo$', index, name='index'),
    url(r'^todo/new$', todo_new, name='new_todo'),
]
