from celery.decorators import task
from celery.utils.log import get_task_logger
from connector.connector import Connector
from celery import task
from .models import Picture
logger = get_task_logger(__name__)


@task
def call_connector_task(tag_name,start_date,end_date):
	""" call connector with args.
	"""
	connector = Connector()
	logger.info("call connector with tag_name: %s,start_date: %s,end_date: %s",tag_name,start_date,end_date)
	data = connector.process_task(tag_name,start_date,end_date)
	for pic in data:
		p = Picture()
		p.save_picture(pic)