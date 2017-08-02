# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import MenuItem
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.views import login as view_login
from django.contrib.auth.views import logout as view_logout
from django.contrib.auth.views import password_change, PasswordChangeDoneView, password_reset, PasswordResetDoneView

menu = MenuItem.objects.order_by('id')

from django.contrib.auth.decorators import login_required


@login_required(login_url=reverse_lazy('common:login'))
def index(request):
    return render(request, 'common/index.html')


def logout(request):
    view_logout(request)
    return redirect(reverse_lazy('common:login'))


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!', extra_tags='alert alert-success')
            return redirect(reverse_lazy('common:change_password'))
        else:
            messages.error(request, 'Please correct the error below.', extra_tags='alert alert-danger')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'common/password_change.html', {'form': form})


class LoginView(FormView):
    http_method_names = ['get', 'post']
    form_class = AuthenticationForm
    template_name = 'common/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
        return view_login(self.request)
