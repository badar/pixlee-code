import re
import sys
import json
import datetime
from urllib.request import Request, urlopen
import urllib.request as urllib2
from datetime import datetime
from time import mktime


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
			date format: datetime object
		"""
		return mktime(date.timetuple())

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
			start_date = self.get_unix_timestamp_given_string(start_date)
		if end_date is None:
			end_date = self.get_unix_timestamp_given_datetime(datetime.now())
		else:
			end_date = self.get_unix_timestamp_given_string(end_date)

		url = base_url + "&min_timestamp="+ str(start_date) + "&max_timestamp="+str(end_date)
		return url


	def parse_data(self,raw_data):
		""" given raw data, parse to extract following values
			to store in db. 
		"""
		data = []
		for val in raw_data:
			if val is not None:
				entry = {}
				entry["date"] = val.get("created_time",None)
				entry["id"] = val.get("id",None)
				entry["link"] = val.get("link",None)
				data.append(entry)
		return data

	def callApi(self,tag_name,start_date,end_date):
		""" given start and end date and tagname - make 
			api call to instagram and return raw data.
		"""
		access_token = ACCESS_TOKEN 
		client_secret = CLIENT_SECRET
		
		result = []
		url = self.construct_url(tag_name,start_date,end_date)
		
		req = Request(url)
		response = urllib2.urlopen(req)
		json_data = json.loads(response.read().decode('utf-8'))
		result.extend(json_data["data"])
		
		while url is not None:
			if "next_url" in json_data["pagination"]:
				url = json_data["pagination"].get("next_url",None)
				response = urllib2.urlopen(url)
				json_data = json.loads(response.read().decode('utf-8'))
				result.extend(json_data["data"])
			else:
				url = None
		
		return result


	def process_task(self,tag_name,start_date,end_date):
		raw_data = self.callApi(tag_name,start_date,end_date)
		data = self.parse_data(raw_data)
		return data
		
		
		
		


if __name__ == "__main__":
	connector = Connector()
	connector.process_task('#stanza','2015-8-19','2015-8-19')

