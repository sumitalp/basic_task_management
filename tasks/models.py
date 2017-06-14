from django.db import models
from django.conf import settings
from datetime import datetime


class Task(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='task_created_by')
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	due_date = models.DateField(blank=True, null=True, )
	completed = models.BooleanField(default=None)
	completed_date = models.DateField(blank=True, null=True)
	assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='assigned_to')

	# Has due date for an instance of this object passed?
	def overdue_status(self):
	    "Returns whether the task's due date has passed or not."
	    if self.due_date and datetime.date.today() > self.due_date:
	        return 1

	def __str__(self):
	    return self.name

	# def get_absolute_url(self):
	#     return reverse('todo-task_detail', kwargs={'task_id': self.id, })

	# Auto-set the item creation / completed date
	def save(self):
	    # If Item is being marked complete, set the completed_date
	    if self.completed:
	        self.completed_date = datetime.datetime.now()
	    super(Task, self).save()
