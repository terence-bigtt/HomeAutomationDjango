# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .forms import ToDoForm, TaskForm, TaskStatusForm
from .models import ToDo, Task, TaskStatus
from django.shortcuts import render, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('common:login'))
def index(request):
    user = request.user
    user_todo = get_list_or_404(ToDo, owner=user)
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
            task_form = TaskForm
            return render(request, 'notes/todo_create.html', {'todo': todo, 'task_form': task_form, 'step': 1})
        if request.POST.get("action") == "create_task":
            todo = ToDo.objects.get(id=request.POST.get("todo_id"))
            todo, task = insert_task(request, todo)
            previous_tasks = Task.objects.filter(todo=todo)
            task_form = TaskForm
            return render(request, 'notes/todo_create.html', {'todo': todo, 'tasks': previous_tasks, 'task_form': task_form, 'step': 1})


def insert_todo(request):
    todo = ToDo(name=request.POST.get("name"), priority=request.POST.get("priority"), owner=request.user)
    todo.save()
    return todo


def insert_task(request, todo):
    post = request.POST

    task = Task(name=post.get("name"), todo=todo, due_date=post.get("due_date"), owner=request.user)
    task.save()
    for assignee in post.get("assigned_to"):
        assignee_user=get_user_by_id(assignee)
        task.assigned_to.add(assignee_user)
    task.save()
    TaskStatus.objects.create(set_by=request.user, task=task)

    return todo, task

def get_user_by_id(id):
    return User.objects.get(id=id)