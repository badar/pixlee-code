from celery.decorators import task
from celery.utils.log import get_task_logger
from connector.connector import Connector
from celery import task
from .models import Picture
from .models import Task
from .models import States
logger = get_task_logger(__name__)


@task(acks_late=True,rate_limit="1000/h")
def call_connector_task(task_id):
	""" call connector with args.
	"""
	connector = Connector()
	logger.info("call connector with task_id: %s",task_id)
	
	task = Task.objects.get(id=task_id)
	if task.status == States.DONE:
		return
	if task.status == States.PROCESSING:
		Picture.objects.filter(task_id=task.id).delete()
	else:
		task.status = States.PROCESSING
		task.save()
	try:
		data = connector.process_task(task)
	except Exception as e:
		call_connector_task.retry(args=(task_id),countdown=60,exec=e,max_retries=2)

	for pic in data:
		p = Picture(link=pic["link"],pic_id=pic["id"],created_date=pic["date"],task=task)
		p.save()

	task.status = States.DONE
	task.save()