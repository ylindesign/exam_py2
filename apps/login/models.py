from __future__ import unicode_literals

from django.db import models
# from ..task.models import Task

import re, md5

PW_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')


class UserManager(models.Manager):
  	def Regis(self, person):
		response = {}
		errors = []
		if len(person['name']) < 3:
			errors.append('Name needs to be at least 3 characters')
		if len(person['password']) < 8:
			errors.append('Password must be at least 8 characters')
		if not (person['password']) == (person['conf_pw']):
			errors.append('Passwords must match!')
		if User.objects.filter(email = person['email']):
			errors.append('Email is taken!')		
		if len(person['dob']) < 1:
			errors.append('Date of Birth cant be left blank')
		if errors:
			response['status'] = False
			response['errors'] = errors
		else:
			hashed_pw = md5.new(person['password']).hexdigest()
			print "hashed_pw at regis", hashed_pw
			response['status'] = True
			response['person'] = self.create(name=person['name'], email=person['email'], dob=person['dob'], password=hashed_pw)
		return response

	def Login(self, person): #Coming in as request.POST
		response = {}
		try:
			user = self.get(email=person['email_login'])
			print user
			login_hash = md5.new(person['pw_login']).hexdigest()
			print "login hash:", login_hash
			print "user password:", user.password
			print "user username:", user.name

			if user.password == login_hash:
				print "passwords match!"
				response['status'] = True
				response['user'] = user
				return response
			else:
				response ['status'] = False
				return response
		except:
			print "failed!!!"

class User(models.Model):
    name = models.CharField( max_length = 255 )
    email = models.CharField( max_length = 255 )
    password = models.CharField( max_length = 255 )
    dob = models.DateField()
    created_at = models.DateTimeField( auto_now_add = True )
    updated_at = models.DateTimeField( auto_now = True )

    objects = UserManager()