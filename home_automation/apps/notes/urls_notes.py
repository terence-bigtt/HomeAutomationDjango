from django.conf.urls import url, include
from django.urls import reverse_lazy
from .views_notes import todo_new, preview_todo, index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^new$', todo_new, name='new_todo'),
    url(r'^(?P<todo_id>\w+)/preview$', preview_todo, name="preview_todo")
]
