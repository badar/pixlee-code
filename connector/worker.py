from models.py import Task
from connector.py import Connector

class Worker:

	def __init__(self):
		self.connector = Connector()

	def run(self):
		task = Task()
		while True:
			tasks = Task.objects.filter(status="NEW")
			for task in tasks:
				self.connector.process_task(task)
					# Change state to Completed
					# save back task




if __name__ == "__main__":
	worker = Worker()
	worker.run()