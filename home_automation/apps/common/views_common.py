# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import MenuItem

menu = MenuItem.objects.order_by('id')


def index(request):
    return render(request, 'common/index.html')
