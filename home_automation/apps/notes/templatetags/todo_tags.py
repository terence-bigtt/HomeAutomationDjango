from django import template
from ..models import ToDo, TaskPriorityOptions

register = template.Library()


@register.filter("priority_name")
def priority_name(value):
    choices = {k: v for k, v in TaskPriorityOptions.choices}
    return choices.get(value, 'Unknown')

@register.filter("assignees")
def assignees(users):
    try:
        names = [user.name for user in users]
        return ", ".join(names)
    except Exception as e:
        print(e)
        return ''


@register.inclusion_tag("notes/user_todo_actions.html", takes_context=True, name="user_todo_actions")
def user_todo_actions(context):
    """
    Must have a user, a todo in the context. Todo Form must have id = todo_form.
    :param context:
    :return:
    """
    user = context["user"]
    todo_id = context["todo"].id
    owns_todo = own_todo(user, todo_id)
    return {"owns_todo": owns_todo}


@register.inclusion_tag("notes/update_todo_form.html", takes_context=True, name="edit_todo")
def edit_todo(context):
    user = context["user"]
    todo_id = context["todo"].id
    owns_todo = own_todo(user, todo_id)
    return {"owns_todo": owns_todo}


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
