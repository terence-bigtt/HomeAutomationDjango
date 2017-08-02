# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import ToDo, Task, TaskStatus

# Register your models here.
admin.site.register(ToDo)
admin.site.register(Task)
admin.site.register(TaskStatus)
