from .models import TaskPriorityOptions


def global_settings(request):
    return {'TASK_PRIORITIES': TaskPriorityOptions.choices}
