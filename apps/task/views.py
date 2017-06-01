from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse

from django.contrib import messages
from .models import Task
import datetime


def task(request):
	if not 'name' in request.session:
		messages.add_message(request, messages.SUCCESS, "Can't skip login!")
		return redirect('/')
	context = {
		'current': Task.objects.filter(date__lte=datetime.date.today()).order_by(),
		'future': Task.objects.filter(date__gt=datetime.date.today()),
		'now': datetime.date.today()
		# 'all': Task.objects.all(),
	}
	return render(request, 'task/task.html', context)

def add(request):
	if request.method == "POST":
		id = request.session['id']
		add_task = {
			'date': request.POST['date'],
			'time': request.POST['time'],
			'task': request.POST['task'],
			'person': id,
		}	

	response = Task.objects.Add(add_task)

	if response['thing'] == False:
		for error in response['errors']:
			messages.add_message(request, messages.ERROR, error)
		return redirect("task:task")
	else:
		messages.add_message(request, messages.SUCCESS, "Task Added!" )
	return redirect('task:task')

def delete(request, id):
	Task.objects.DeleteTask(id)
	return redirect('task:task')

def edit(request, id):
	info = Task.objects.get(id=id)
	stuff = {
		'info': info,
	}	
	return render(request, 'task/edit.html', stuff)

def update(request, id):
	if request.method == "POST":
		# id = request.session['id']
		update_task = {
			'date': request.POST['date'],
			'time': request.POST['time'],
			'task': request.POST['task'],
			'status': request.POST['status'],
			# 'id': id,
		}
	response = Task.objects.Update(update_task)

	if response['status'] == False:
		for error in response['errors']:
			messages.add_message(request, messages.ERROR, error)
		return redirect( reverse("edit") )
	else:
		Task.objects.get(id=id).update(task=update_task['task'], date=update_task['date'], time=update_task['time'])
		messages.add_message(request, messages.SUCCESS, "Task Updated!" )
	return redirect('task:task')



