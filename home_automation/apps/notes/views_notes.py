# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import ToDoForm, TaskForm, TaskStatusForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('common:login'))
def index(request):
    return "should show current users assigned tasks and owned todos"

def preview_todo(request):
    return 'should show the todo, tasks, users and status history'

@login_required(login_url=reverse_lazy('common:login'))
def todo_new(request):
    form1 = ToDoForm()
    form2 = TaskForm()
    form3 = TaskStatusForm()
    return render(request, 'notes/todo_create.html', {'form1': form1, 'form2': form2, 'form3': form3})

