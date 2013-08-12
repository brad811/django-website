from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import hashlib, random, string

from website.models import User

def index(request):
	if is_logged_in(request):
		return render(request, 'website/home.html', {
			'users_list': User.objects.all(),
		})
	else:
		return render(request, 'website/index.html', {
			'users_list': User.objects.all(),
		})

def is_logged_in(request):
	cookie = request.COOKIES.get('user', '')
	try:
		id = cookie.split(',')[0]
		password_hash = cookie.split(',')[1]
		user = User.objects.get(id=id)
	
		if hashlib.sha256(user.password).hexdigest() != password_hash:
			return False
		else:
			return True
	except (ObjectDoesNotExist, IndexError) as e:
		return False

def login(request):
	if request.method == "GET":
		return HttpResponseRedirect(reverse('index'))
	
	response = validate_login(request)
	
	if response.content == "valid":
		# check if "remember me" was checked in the future
		# , httponly=True
		user = User.objects.get(email=request.POST.get('login_email',''))
		value = str(user.id) + ',' + hashlib.sha256(user.password).hexdigest()
		
		if request.POST.get('remember_me','false') == "true":
			response.set_cookie('user', value, max_age=3600*24*30)
		else:
			response.set_cookie('user', value)
		
	
	return response

def validate_login(request):
	login_email = request.POST.get('login_email','')
	login_password = request.POST.get('login_password','')
	
	if len(login_email) == 0:
		return HttpResponse("error,You forgot to enter an email address!")
	elif len(login_password) == 0:
		return HttpResponse("error,You forgot to enter a password!")
	else:
		try:
			user = User.objects.get(email=login_email)
			salt = user.password.split(',')[1]
		except User.DoesNotExist:
			user = None
			
		if user == None or user.password != hashlib.sha256(login_password + salt).hexdigest() + "," + salt:
			return HttpResponse("error,The email or password you entered was incorrect!")
		
		response = HttpResponse("valid")
		
	return response

def logout(request):
	response = HttpResponseRedirect(reverse('index'))
	response.delete_cookie('user')
	return response

def register(request):
	if request.method == "GET":
		return HttpResponseRedirect(reverse('index'))
	
	signup_name = request.POST.get('signup_name','')
	signup_email = request.POST.get('signup_email','')
	signup_password = request.POST.get('signup_password','')
	user = User(name=signup_name, email=signup_email, password=signup_password)
	result = validate_registration_data(user)
	if result == "valid":
		salt = ''.join(random.choice(string.letters) for x in xrange(5))
		user.password = hashlib.sha256(signup_password + salt).hexdigest() + "," + salt
		user.save()
		
		newRequest = HttpRequest()
		newRequest.POST['login_email'] = signup_email
		newRequest.POST['login_password'] = signup_password
		return login(newRequest)
	else:
		return HttpResponse(result)

def validate_registration_data(user):
	if len(user.email) < 1:
		return "error,You must enter an email address."
	try:
		validate_email(user.email)
	except ValidationError:
		return "error,The email address entered is invalid."
	if User.objects.filter(email=user.email).count() > 0:
		return "error,The email address entered is already registered."
	if len(user.password) < 8:
		return "error,The password must be at least 8 characters."
	if len(user.name) < 1:
		return "error,You must enter a name."
	
	return "valid"
