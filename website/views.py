from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib import auth
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser

from website.models import User

def index(request):
	try:
		request.user = User.objects.get(pk=request.session.get('_auth_user_id'))
	except User.DoesNotExist:
		request.user = AnonymousUser()
	
	if request.user.is_authenticated():
		return render(request, 'website/home.html', {
			'users_list': User.objects.all(),
		})
	else:
		return render(request, 'website/index.html', {
			'users_list': User.objects.all(),
		})

def login(request):
	if request.method == "GET":
		return HttpResponseRedirect(reverse('index'))
	
	login_email = request.POST.get('login_email','')
	login_password = request.POST.get('login_password','')
	
	if len(login_email) == 0:
		return HttpResponse("error,You forgot to enter an email address!")
	elif len(login_password) == 0:
		return HttpResponse("error,You forgot to enter a password!")
	
	user = User.objects.authenticate(email=login_email, password=login_password)
	
	if user is None:
		return HttpResponse("error,The email or password you entered was incorrect!")
	
	auth.login(request, user)
	
	return HttpResponse("valid")

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('index'))

def register(request):
	if request.method == "GET":
		return HttpResponseRedirect(reverse('index'))
	
	signup_name = request.POST.get('signup_name','')
	signup_email = request.POST.get('signup_email','')
	signup_password = request.POST.get('signup_password','')
	
	try:
		User.objects.create_user(signup_name, signup_email, signup_password)
	except ValueError as e:
		return HttpResponse('error,' + str(e))
	
	newRequest = HttpRequest()
	newRequest.session = request.session
	newRequest.POST['login_email'] = signup_email
	newRequest.POST['login_password'] = signup_password
	
	return login(newRequest)
