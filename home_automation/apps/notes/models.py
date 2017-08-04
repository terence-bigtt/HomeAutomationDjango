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


class ToDo(models.Model):
    name = models.CharField(max_length=80)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.TimeField(default=timezone.now)
    priority = models.CharField(max_length=1, choices=TaskPriorityOptions.choices, default=TaskPriorityOptions.LOW)

    def __str__(self):
        return "ToDo {}: {}".format(self.id, self.name)


class Task(models.Model):
    name = models.CharField(max_length=80)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='owner_user')
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    due_date = models.DateField(default=timezone.now() + timezone.timedelta(days=7))
    created_at = models.DateField(default=timezone.now)
    assigned_to = models.ManyToManyField(User, related_name='assigned_to_users')
    priority = models.CharField(max_length=1, choices=TaskPriorityOptions.choices, default=TaskPriorityOptions.LOW)

    def __str__(self):
        return "Task {}: {}".format(self.id, self.name)

class TaskStatus(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=TaskStatusOptions.choices, default=TaskStatusOptions.WAITING)
    created_at = models.DateField(default=timezone.now)
    set_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "TaskStatus{}: {} - {}".format(self.id, self.task.name, self.status)
