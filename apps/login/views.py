from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse

from django.contrib import messages
from .models import User

def index(request):
	if 'name' in request.session:
		return redirect('task:task')
	return render(request, 'login/index.html')

def register(request):
	person = {
		'name': request.POST['name'],
		'email': request.POST['email'],
		'password': request.POST['password'],
		'conf_pw': request.POST['conf_pw'],
		'dob': request.POST['dob'],
	}

	if request.method != "POST":
		messages.add_message(request, messages.ERROR, "Cant have an empty form")
		return redirect("/")

	response = User.objects.Regis(person)

	if response['status'] == False:
		for error in response['errors']:
			messages.add_message(request, messages.ERROR, error)
		return redirect("/")
	else:
		messages.add_message(request, messages.SUCCESS, "You have registered!" )
		request.session['name'] = person['name']
		request.session['id'] = response['person'].id
	return redirect('task:task')


def login(request):
	if request.method != "POST":
		messages.add_message(request, messages.ERROR, "Must be logged in")
		return redirect('/')
	# print "name: ", len(request.POST['email_login'])
	# print "pw: ", len(request.POST['pw_login'])
	if request.method == "POST":
		if len(request.POST['email_login']) < 1 or len(request.POST['pw_login']) < 1:
			messages.add_message(request, messages.ERROR, 'Email and/or Password cant be left blank')
			return redirect('/')

		response = User.objects.Login(request.POST)
		
		if response['status'] == True:
			print "name: ", response['user'].name
			print "id: ", response['user'].id
			request.session['name'] = response['user'].name
			request.session['id'] = response['user'].id
		return redirect('task:task')
	else:
		for error in response['errors']:
			messages.error(request, error)
	return redirect('/')

def logout(request):
	request.session.flush()
	return redirect('/')