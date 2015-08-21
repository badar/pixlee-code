#@author: Osama Badar
import re
import sys
import json
import datetime
from datetime import datetime
from time import mktime
import requests
import logging

CLIENT_SECRET = "381f55a0c1fd421aa8fe49bcf8f1daa8"
ACCESS_TOKEN = "503340310.f116fce.069c8ad42d1c49f1a2476333bd9432b4"
START_DATE = "2015-08-15"

class Connector:
	""" connects to Instagram API and pulls data from API.
	"""
	def get_unix_timestamp_given_string(self,date):
		""" given a string, convert to unix timestamp.
			date format: Y-M-D.
		"""
		date = date.split(" ")[0]
		return mktime(datetime.strptime(date, "%Y-%m-%d").timetuple())

	def get_unix_timestamp_given_datetime(self,date):
		""" given a string, convert to unix timestamp.
			date format: datetime object.
		"""
		return mktime(date.timetuple())

	def get_datetime_from_unix(self,date):
		""" given unixtimestamp get datetime object.
		"""
		return datetime.fromtimestamp(int(date))

	def get_string_date_from_datetime(self,date):
		""" given datetime convert to string date
		"""
		return date.strftime('%Y-%M-%D')

	def construct_url(self,tag_name,start_date,end_date):
		""" given a tagname and start_date and end_date construct a url.
		"""
		if tag_name is None:
			raise ValueError("tag_name is None!")

		if tag_name[0] == "#":
			tag_name = tag_name[1:]

		base_url = "https://api.instagram.com/v1/tags/"+tag_name+"/media/recent?access_token="+ACCESS_TOKEN
		if start_date is None:
			start_date = self.get_unix_timestamp_given_string(START_DATE)
		else:
			start_date = self.get_unix_timestamp_given_datetime(start_date)
		if end_date is None:
			end_date = self.get_unix_timestamp_given_datetime(datetime.now())
		else:
			end_date = self.get_unix_timestamp_given_datetime(end_date)

		return (base_url,start_date,end_date)

	def parse_data(self,raw_data):
		""" given raw data, parse to extract following values
			to store in db. 
		"""
		data = []
		for val in raw_data:
			if val is not None:
				entry = {}
				entry["date"] = self.get_datetime_from_unix(val.get("created_time",None))
				entry["id"] = val.get("id",None)
				entry["link"] = val.get("link",None)
				data.append(entry)
		return data

	def call_api(self,tag_name,start_date,end_date):
		""" given start and end date and tagname - make 
			api call to instagram and return raw data.
		"""
		access_token = ACCESS_TOKEN 
		client_secret = CLIENT_SECRET
		
		result = []
		url,start_date,end_date = self.construct_url(tag_name,start_date,end_date)
		start_date = self.get_datetime_from_unix(start_date)
		end_date = self.get_datetime_from_unix(end_date)
		r = requests.get(url)
		json_data = r.json()
		data = json_data["data"]
		for val in data:
			created_date = self.get_datetime_from_unix(val.get("created_time"))
			if created_date >= start_date and created_date <= end_date:
				result.append(val)
		while url is not None:
			if "next_url" in json_data["pagination"]:
				url = json_data["pagination"].get("next_url",None)
				r = requests.get(url)
				json_data = r.json()
				data = json_data["data"]
				for val in data:
					created_date = self.get_datetime_from_unix(val.get("created_time"))
					if created_date >= start_date and created_date <= end_date:
						result.append(val)
			else:
				url = None
		return result

	def process_task(self,task):
		""" called by celery to run each request asynchronouly.
		"""
		startTime = datetime.now()
		tag_name = task.tag_name
		start_date = task.start_date
		end_date = task.end_date
		_id = task.id
		logging.info("processing task with id:%s, tag_name:%s, start_date:%s and end_date:%s",_id,tag_name,start_date,end_date)
		raw_data = self.call_api(tag_name,start_date,end_date)
		data = self.parse_data(raw_data)
		endTime = datetime.now()
		timedelta = endTime - startTime
		return data
			
if __name__ == "__main__":
	connector = Connector()


