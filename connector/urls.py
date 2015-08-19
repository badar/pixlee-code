from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.tasks, name='tasks'),
	url(r'^task/new/$', views.post_task, name='post_task'),

]