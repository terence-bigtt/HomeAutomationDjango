from django import forms
from .models import ToDo, Task, TaskStatus


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ('name', 'priority')


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'assigned_to', 'priority', 'due_date')


class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = TaskStatus
        fields = ('status',)
