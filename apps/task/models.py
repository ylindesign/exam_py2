from __future__ import unicode_literals

from django.db import models
from ..login.models import User
from datetime import datetime
from time import strftime


class taskManager(models.Manager):
  	def Add(self, add_task):
  		response = {}
		errors = []
		if len(add_task['date']) == 0 or not add_task['time'] or len(add_task['task']) == 0:
			errors.append('Nothing can be blank')
			response['thing'] = False
			response['errors'] = errors
			if len(add_task['date']) > 1: 
				if add_task['date'] < "2017-06-01":
					errors.append('Cant make appointment for the past')
					response['thing'] = False
					response['errors'] = errors
		else:
			person = User.objects.get(id=add_task['person'])
			# new_time = datetime.strftime(add_task['time'], "%H:%M")
			self.create(task=add_task['task'], date=add_task['date'], time=add_task['time'], user=person)
			response['thing'] = True
		return response

	def DeleteTask(self, id):
		self.get(id=id).delete()
		pass

	def Update(self, update_task):
  		response = {}
		errors = []
		if len(update_task['date']) < 1 or len(update_task['time']) < 1 or len(update_task['task']) < 1:
			errors.append('Nothing can be blank')
			response['status'] = False
			response['errors'] = errors
			return response
		elif len(update_task['date']) > 1: 
			if update_task['date'] < "2017-06-01":
				errors.append('Cant make appointment for the past')
				response['status'] = False
				response['errors'] = errors
				return response
		# else:
		# token = Task.objects.get(id=update_task['id'])
		# token.update(task=add_task['task'], date=add_task['date'], time=add_task['time'])
			# new.task = update_task['task']
			# new.date = update_task['date']
			# new.time = update_task['time']
			# new.status = update_task['status']
			# new.save()
		response['status'] = True
		return response

class Task(models.Model):
	task = models.CharField(max_length = 255)
	date = models.DateField()
	time = models.TimeField()
	user = models.ForeignKey(User, related_name = 'user')
	status = models.CharField(max_length = 255, default="Pending" )
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = taskManager()