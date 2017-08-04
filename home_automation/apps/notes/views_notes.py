# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

from .forms import ToDoForm, TaskForm, TaskStatusForm
from .models import ToDo, Task


@login_required(login_url=reverse_lazy('common:login'))
def index(request):
    user = request.user
    user_todo = ToDo.objects.filter(owner=user)
    user_tasks = Task.objects.filter(assigned_to__in=[user])

    return render(request, 'notes/index.html', {'todos': user_todo, 'tasks': user_tasks})


@login_required(login_url=reverse_lazy('common:login'))
def preview_todo(request):
    form2 = TaskForm()
    form3 = TaskStatusForm()


@login_required(login_url=reverse_lazy('common:login'))
def todo_new(request):
    if request.method == "GET":
        todo_form = ToDoForm()
        return render(request, 'notes/todo_create.html', {'form1': todo_form, 'step': 0})
    if request.method == "POST":
        if request.POST.get("action") == "create_todo":
            todo = insert_todo(request)
            task_form = TaskForm(initial={"owner": request.user})
            return render(request, 'notes/todo_create.html', {'todo': todo, 'task_form': task_form, 'step': 1})
        if request.POST.get("action") == "create_task":
            todo = ToDo.objects.get(id=request.POST.get("todo_id"))
            insert_task(request, todo)
            previous_tasks, task_form = refresh_tasks(request, todo)
            return render(request, 'notes/todo_create.html',
                          {'todo': todo, 'tasks': previous_tasks, 'task_form': task_form, 'step': 1})
        if request.POST.get("action") == "delete_task":
            delete_task(request)
            todo = ToDo.objects.get(id=request.POST.get("todo_id"))
            previous_tasks, task_form = refresh_tasks(request, todo)
            return render(request, 'notes/todo_create.html',
                          {'todo': todo, 'tasks': previous_tasks, 'task_form': task_form, 'step': 1})


def refresh_tasks(request, todo):
    previous_tasks = Task.objects.filter(todo=todo)
    task_form = TaskForm()
    return previous_tasks, task_form


def insert_todo(request):
    todo_form = ToDoForm(request.POST)
    if todo_form.is_valid():
        todo = todo_form.save(commit=False)
        todo.owner = request.user
        todo.save()
    return todo


def insert_task(request, todo):
    task_form = TaskForm(request.POST)
    if task_form.is_valid():
        data = task_form.cleaned_data
        task = Task(owner=request.user, name=data["name"], due_date=data["due_date"], priority=data["priority"],
                    todo=todo, )
        task.save()
        task.assigned_to = data['assigned_to']
        task.save()
    else:
        messages.error(request, 'Please correct the error below.', extra_tags='alert alert-danger')


def delete_task(request):
    task_id = request.POST.get("task_id")
    Task.objects.get(id=task_id).delete()
