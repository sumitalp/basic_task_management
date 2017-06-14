from django.conf import settings

STAFF_ONLY = getattr(settings, 'TASK_STAFF_ONLY', False)
DEFAULT_LIST_ID = getattr(settings, 'TASK_DEFAULT_LIST_ID', 1)
DEFAULT_ASSIGNEE = getattr(settings, 'TASK_DEFAULT_ASSIGNEE', None)
PUBLIC_SUBMIT_REDIRECT = getattr(settings, 'TASK_PUBLIC_SUBMIT_REDIRECT', '/')