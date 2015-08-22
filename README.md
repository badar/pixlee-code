# pixlee-code
Pixlee coding challenge.

To Run:
Fire django server and go to:
http://localhost:8000/task/new/.
Enter: #tagname, start_date and end_date

Dependency:
Django,Postgres,Python3.0,Celery,Redis.

System Analysis:

1- The system runs a Django app called "connector". I installed celery with reddis as message broker to run all requests 
asynchrounously. Celery runs all tasks in parallel and if required, can always set it to run multiple workers instead of one worker.Tasks are created by each request to the server. Tasks consist of tagname , start_date and end_date. Each task has unique id and is stored in postgresDB. This is independent of how redis stores celery tasks.
A task can exist in 3 states namely: "NEW", "PROCESSING" and "DONE". 
If the api_request throws an exception?
Retry the request in case of exception after every minute so countdown=60 and max_tries=3.
If the system dies, how do you recover from the last point the collection occurred?
I have set celery's "CELERY_ACKS_LATE" = True, which ensures that each request is acknowledged and so every task is retried if worker crashes until ack is received. If the worker crashes, requests will be retried. There are 3 cases for a retried request:
a-Worker crashed after job was finished so if task being retried is in DONE state, just return. 
b-If the task being retried is in PROCESSING state: worker could have crashed before api call was complete or just in the middle of writing photos to db. We delete all pictures associated with that unique task id and retry the request.
c-Otherwise the task is in state NEW so change state to PROCESSING and call connector.

How to minimize the amount of API hits, and thus minimize the chance of hitting the rate limit on the token?
Instagram API allows 5000 req/hour so I have set a rate_limit on celery to avoid too many tasks requests.I chose an arbitrary number but more thought needs to be put into this.
If the Date is in future what should be done?
I didn't implement this but ideally if date is in future, we can do 2 things:
a) Change the end date to datetime.now()
b) Break the task into 2 parts - one uptil today's date and fetch it and the second task should be run at a later date with a timer set in celery - possibly every day uptill the end_date.

Analysis of Connector:

1- Connector App resides in project Pixlee. Connector.py makes API calls to Instagram API to fetch pictures based on 
tagname, start_date and end_date provided to it.
2- Sanitize tagname by removing "#" tag from word. Timestamp passed in by Django View is a string object, "Y-M-D.." that is stripped and coverted to datetime object for comparison. Since the tag API doesn't provide any way to get pics within given time period, I do date range check on the fly and create a list of pics that fall in the date range provided and store them to postgres collection Picture.
3- API calls are made using python Request library. Each response contains pagination information and data so we paginate until 
 "next_url" that is embedded in pagination info returns None. 

Data Storage:

Data is parsed and stored in postgres db in 2 tables. 
1-Picture - link, pic_id, created_date, Task[foriegn key for task] - Task id is stored with each picture so if worker crashes and we retry, we should delete all pictures and fetch them again. Ideally, we should have a mechenism that we start from where the last pic was fetched.
2-Task - tag_name,start_date, end_date,status. Task can exist in 3 states namely NEW, PROCESSING and DONE.






