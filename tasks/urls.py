from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add/$', views.add_task, name="add_task"),
    url(r'^detail/(?P<task_id>\d{1,6})$', views.view_task, name="task_detail"),
    url(r'^delete/(?P<task_id>\d{1,6})$', views.del_list, name="task_delete"),
    url(r'^$', views.task_lists, name="task-lists"),
]
