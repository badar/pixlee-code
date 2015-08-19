from django.shortcuts import render
from .forms import TaskForm
from .models import Task
from .models import Picture
from .connector import Connector
from .tasks import call_connector_task



def tasks(request):
	return render(request, 'connector/tasks.html', {})

def post_task(request):
    
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
        tag_name = request._post.get("tag_name")
        start_date = request._post.get("start_date")
        end_date = request._post.get("end_date")
        call_connector_task.delay(tag_name,start_date,end_date)
       

    return render(request, 'connector/post_task.html', {'form': form})


