from django import template
from ..models import ToDo

register = template.Library()


@register.filter("owns_todo")
def owns_todo(user, todo_id):
    return own_todo(user, todo_id)


@register.filter("not_owns_todo")
def not_owns_todo(user, todo_id):
    return not owns_todo(user, todo_id)


def own_todo(user, todo_id):
    try:
        todo = ToDo.objects.get(id=todo_id)
        owner = todo.owner
        return owner == user
    except Exception as e:
        print(e)
        return False
