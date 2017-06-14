import datetime

from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.sites.models import Site

from tasks import settings
from tasks.forms import AddTaskForm, EditTaskForm
from tasks.models import Task
# from todo.utils import mark_done, undo_completed_task, del_tasks, send_notify_mail

# Need for links in email templates
# current_site = Site.objects.get_current()


def check_user_allowed(user):
    """
    Conditions for user_passes_test decorator.
    """
    if settings.STAFF_ONLY:
        return user.is_authenticated() and user.is_staff
    else:
        return user.is_authenticated()


@user_passes_test(check_user_allowed)
def task_lists(request):
    """
	Homepage view - list of lists a user can view, and ability to add a list.
	"""

	# Superusers see all lists
    if request.user.is_superuser:
        task_list = Task.objects.all().order_by('name')
    else:
        task_list = Task.objects.filter(Q(assigned_to=request.user) | Q(created_by=request.user))

    return render(request, 'tasks/lists.html', locals())

@user_passes_test(check_user_allowed)
def add_task(request, *args, **kwargs):
    """
    Allow users to add new task
    """

    if request.POST:
        form = AddTaskForm(request.user, request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "A new task has been added.")
                return HttpResponseRedirect(request.path)
            except IntegrityError:
                messages.error(
                    request,
                    "There was a prbolem saving the new task"
                )
    else:
        form = AddTaskForm(request.user)

    return render(request, 'tasks/add_task.html', locals())


@user_passes_test(check_user_allowed)
def view_task(request, task_id):
    """
    View task details. Allow task details to be edited.
    """
    task = get_object_or_404(Task, pk=task_id)

    # Ensure user has permission to view item.
    # Get the users this task belongs to.
    # Admins can edit all tasks.

    if task.assigned_to == request.user or request.user.is_staff:
        auth_ok = True

        if request.POST:
            form = EditTaskForm(request.POST, instance=task)

            if form.is_valid():
                form.save()

                messages.success(request, "The task has been edited.")

                return HttpResponseRedirect(reverse('tasks:task-lists'))
        else:
            form = EditTaskForm(instance=task)
            if task.due_date:
                thedate = task.due_date
            else:
                thedate = datetime.datetime.now()
    else:
        messages.info(request, "You do not have permission to view/edit this task.")

    return render(request, 'tasks/view_task.html', locals())


@user_passes_test(check_user_allowed)
def del_list(request, task_id):
    """
    Delete an entire task.
    """
    list = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        Task.objects.get(id=list.id).delete()
        messages.success(request, "{list_name} is gone.".format(list_name=list.name))
        return HttpResponseRedirect(reverse('todo-lists'))

    return render(request, 'tasks/del_list.html', locals())
