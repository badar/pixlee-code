# pixlee-code
pixlee coding challenge

To Run:
Fire django server and go to:
http://localhost:8000/task/new/
Add #tagname, start_date and end_date

Dependency:
Django, Postgres, Python3.0, Celery, Redis.

System Analysis:

1- The system runs a Django app called "connector". I installed celery with reddis as message broker to run all requests 
asynchrounously. Celery runs all tasks in parallel and we can always set it to run multiple workers instead of one worker.
Tasks are created by each request to the server. Tasks consist of tagname , start_date and end_date. Each task has uniqe id and is stored in postgresDB. This is independent of how redis stores celery tasks.
A task can exist in 3 states namely: NEW, PROCESSING and DONE. 

How to minimize the amount of API hits, and thus minimize the chance of hitting the rate limit on the token?
Instagram API allows 5000 req/hour so I have set a rate_limit on celery to avoid too many tasks requests.
If the system dies, how do you recover from the last point the collection occurred?
I have set celery CELERY_ACKS_LATE = True, which ensures that each request is ack and so every task is retried. If the worker 
crashes, requests will be retried. Moreover, in tasks.py, there are 3 states: 
1-if task being retried is in DONE state, just return.
2-if the task being retried is in processing, we delete the pictures if they were stored before the crash happened and retry request.
3- If the task is new, change state to processing and call connector.
If the Date is in future:
I didn't implement this but ideally if date is in future, maybe set some timer for task and try it in future.

Analysis of Connector:

1- Connector App resides in project Pixlee. Connector.py uses makes API calls to Instagram API to fetch pictures based on 
tagname, start and end dates provided to it.
2- Sanitize tagname by removing "#" tag from word. Timestamp passed in by Django View is a string object that is coverted to datetime object for comparison. Since the tag API doesn't provide any way to get pics within given time period, i do date range check on the fly and create a list of pics that need to be stored before they are written to postgres.
3- Make API call using python Request lib. Each response contains pagination information and data. 
4- Pagination: Keep calling "next_url" that is embedded in pagination info until there is no "next_url" field.

Data Storage:

Data is parsed and stored in postgres db in 2 tables. 
1-Picture - link, pic_id, created_date, Task[foriegn key for task]
2-Task - tag_name,start_date, end_date.






