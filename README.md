# pixlee-code
pixlee coding challenge

To Run:
Fire django server and go to:
http://localhost:8000/task/new/
Add #tagname, start_date and end_date

Dependency:
Django, Postgres, Python 3.0, Celery, Redis.

System Analysis:

1- The system runs a Django app called "connector". I installed celery with reddis as message broker to run all requests 
asynchrounously. Celery runs all tasks in parallel and we can always set it to run multiple workers instead of one worker.
if the Date is in future, the end date defaults to datetime.now().
How to minimize the amount of API hits, and thus minimize the chance of hitting the rate limit on the token?
TODO?
If the system dies, how do you recover from the last point the collection occurred?
TODO?


Analysis of Connector:

1- Connector App resides in project Pixlee. Connector.py uses makes API calls to Instagram API to fetch pictures based on 
tagname, start and end dates provided to it.
2- Sanitize tagname by removing "#" tag from word. Timestamp passed in by Django View is a string object that is converted to 
unixtimestamp before building a url.
3- Make API call using python urllib lib. Each response contains pagination information and data. 
4- Pagination: Keep calling "next_url" that is embedded in pagination info until there is no "next_url" field.

Data Storage:

Data is parsed and stored in postgres db in 2 tables. 
1-Picture - link, pic_id, created_date.
link: url of the pic
pic_id: unique photo id
created_date: unixtime stamp of pic create date.
2-Task - tag_name,start_date, end_date.
Each Task is stored in db for debugging purposes. 
this is request passed from view.





