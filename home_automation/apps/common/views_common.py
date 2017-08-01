# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import MenuItem
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import login as view_login

menu = MenuItem.objects.order_by('id')


def index(request):
    return render(request, 'common/index.html')


class LoginView(FormView):
    http_method_names = ['get', 'post']
    form_class = AuthenticationForm
    template_name = 'profile/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
        return view_login(self.request)
