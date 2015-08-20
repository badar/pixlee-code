from django.db import models
from django.utils import timezone


class Picture(models.Model):
    """ picture object downloaded from instagram.
    """
    link = models.URLField(max_length=200)
    pic_id = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def save_picture(self,pic):
    	self.link = pic["link"]
    	self.pic_id = pic["id"]
    	self.created_date = pic["date"]
    	self.save()


class Task(models.Model):
	""" Each task has tag_name, start_date and end_date.
		status: [PROCESSING,NEW,DONE]
	"""
	tag_name = models.CharField(max_length=200,blank=True)
	start_date = models.DateTimeField(default=timezone.now)
	end_date = models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length=200,default="NEW")

	def task_save(self,tag_name,start_date,end_date,status):
		self.tag_name = tag_name
		self.start_date = start_date
		self.end_date = end_date
		self.status = status




 


