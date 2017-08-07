# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import ToDoForm, TaskForm, TaskStatusForm
from .models import ToDo, Task


@login_required(login_url=reverse_lazy('common:login'))
def index(request):
    if request.method == 'POST':
        action = request.POST.get("action")
        if action == 'delete_todo':
            try:
                todo_id = request.POST.get("todo_id")
                ToDo.objects.get(todo_id).delete
            except:
                pass
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
        return render(request, 'notes/todo_create.html', {'todo_form': todo_form, 'step': 0})
    if request.method == "POST":
        if request.POST.get("action") == "create_todo":
            return create_todo(request)
        if request.POST.get("action") == "delete_todo":
            return delete_todo(request)
        if request.POST.get("action") == "edit_todo":
            return update_todo(request)
        if request.POST.get("action") == "create_task":
            return create_task(request)
        if request.POST.get("action") == "delete_task":
            return delete_task(request)


def create_todo(request):
    todo = insert_todo(request)
    todo_form = ToDoForm(instance=todo)
    task_form = TaskForm(initial={"owner": request.user})
    return render(request, 'notes/todo_create.html',
                  {'todo': todo, "todo_form": todo_form, 'task_form': task_form, 'step': 1})


def insert_todo(request):
    todo_form = ToDoForm(request.POST)
    if todo_form.is_valid():
        todo = todo_form.save(commit=False)
        todo.owner = request.user
        todo.save()
    return todo


def delete_todo(request):
    try:
        ToDo.objects.get(id=request.POST.get("todo_id")).delete()
    except Exception as e:
        print(e)
        pass
    return redirect(reverse_lazy('notes:index'))


def update_todo(request):
    todo_id = request.POST.get("todo_id")
    todo = ToDo.objects.get(id=todo_id)
    name = request.POST.get("name")
    priority = request.POST.get("priority")
    todo.name = name
    todo.priority = priority
    previous_tasks, task_form, todo_form = refresh_tasks(request, todo)
    todo.save()
    return render(request, 'notes/todo_create.html',
                  {'todo': todo, "todo_form": todo_form, 'tasks': previous_tasks, 'task_form': task_form, 'step': 1})


def create_task(request):
    todo = ToDo.objects.get(id=request.POST.get("todo_id"))
    insert_task(request, todo)
    previous_tasks, task_form, todo_form = refresh_tasks(request, todo)
    return render(request, 'notes/todo_create.html',
                  {'todo': todo, "todo_form": todo_form, 'tasks': previous_tasks, 'task_form': task_form, 'step': 1})


def refresh_tasks(request, todo):
    previous_tasks = Task.objects.filter(todo=todo)
    todo_form = ToDoForm(instance=todo)
    task_form = TaskForm()
    return previous_tasks, task_form, todo_form


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
    todo = ToDo.objects.get(id=request.POST.get("todo_id"))
    previous_tasks, task_form, todo_form = refresh_tasks(request, todo)
    return render(request, 'notes/todo_create.html',
                  {'todo': todo, "todo_form": todo_form, 'tasks': previous_tasks, 'task_form': task_form, 'step': 1})
