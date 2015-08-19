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
    	self.save()


class Task(models.Model):
	""" status : [COMPLETED,PROCESSING,NEW]
	"""
	tag_name = models.CharField(max_length=200,blank=True)
	start_date = models.DateTimeField(default=timezone.now)
	end_date = models.DateTimeField(default=timezone.now)
	



 


