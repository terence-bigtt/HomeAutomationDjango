# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class MenuItem(models.Model):
    caption = models.CharField(max_length=20)
    page = models.CharField(max_length=20)
    target = models.CharField(max_length=20)
    id = models.AutoField(primary_key=True)
