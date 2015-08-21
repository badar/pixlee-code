from django.db import models
from django.utils import timezone

class States:
	NEW = "NEW"
	PROCESSING = "PROCESSING"
	DONE = "DONE"

class Task(models.Model):
	""" Each task has tag_name, start_date and end_date.
		status: [PROCESSING,NEW,DONE]
	"""
	tag_name = models.CharField(max_length=200,blank=True)
	start_date = models.DateTimeField(default=timezone.now)
	end_date = models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length=200,default=States.NEW)


class Picture(models.Model):
    """ picture object downloaded from instagram.
    """
    link = models.URLField(max_length=200)
    pic_id = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    task = models.ForeignKey(Task)









 


