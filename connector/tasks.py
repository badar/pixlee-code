from celery.decorators import task
from celery.utils.log import get_task_logger
from connector.connector import Connector
from celery import task
from .models import Picture
from .models import Task
logger = get_task_logger(__name__)


@task(rate_limit='100/h')
def call_connector_task(task_id):
	""" call connector with args.
	"""
	connector = Connector()
	logger.info("call connector with task_id: %s",task_id)
	
	task = Task.objects.get(id = task_id)
	if task.status == "DONE":
		return
	if task.status == "PROCESSING":
		Picture.objects.get(task).delete()
	else:
		task.status = "PROCESSING"
		task.save()

	try:
		data = connector.process_task(task)
	except Exception as e:
		self.retry(countdown=1000,exec=e,max_retries=2)

	for pic in data:
		p = Picture(link=pic["link"],pic_id=pic["id"],created_date=pic["date"],task=task)
		p.save()

	task.status = "DONE"
	task.save()