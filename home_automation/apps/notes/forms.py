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
        widgets = {'due_date': forms.DateInput(attrs={'class': 'datepicker'})}

class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = TaskStatus
        fields = ('status',)
