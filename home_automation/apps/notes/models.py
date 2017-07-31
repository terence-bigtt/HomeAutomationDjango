# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.


class TaskStatusOptions:
    WAITING = "0"
    STARTED = "1"
    DONE = "2"
    ABORTED = "3"
    CANCELLED = "4"
    choices = ((WAITING, "Waiting"),
               (STARTED, "Started"),
               (DONE, "Done"),
               (ABORTED, "Aborted"),
               (CANCELLED, "Canceled")
               )


class TaskPriorityOptions:
    LOW = "0"
    MEDIUM = "1"
    HIGH = "2"
    choices = ((LOW, "Low"),
               (MEDIUM, "Medium"),
               (HIGH, "High"))


class TaskStatus(models):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=TaskStatusOptions.choices, default=TaskStatusOptions.WAITING)
    created_at = models.TimeField(default=timezone.now())
    set_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Task(models):
    name = models.TextField(max_length=80)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    due_date = models.TimeField(default=timezone.now() + timezone.timedelta(days=7))
    created_at = models.TimeField(default=timezone.now())
    assigned_to = models.ManyToManyField()
    priority = models.CharField(max_length=1, choices=TaskPriorityOptions.choices, default=TaskPriorityOptions.LOW)


class ToDo(models):
    name = models.TextField(max_length=80)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.TimeField(default=timezone.now())
    priority = models.CharField(max_length=1, choices=TaskPriorityOptions.choices, default=TaskPriorityOptions.LOW)
