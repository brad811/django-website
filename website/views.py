from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib import auth

from website.models import User
from website.decorators import get_user, login_required, anonymous_required, post_required

def index(request):
	if get_user(request).is_authenticated():
		return render(request, 'website/home.html', {
			'users_list': User.objects.all(),
		})
	else:
		return render(request, 'website/index.html', {
			'users_list': User.objects.all(),
		})

@login_required()
def settings(request):
	return render(request, 'website/settings.html')

@post_required()
@anonymous_required()
def login(request):
	login_email = request.POST.get('login_email','')
	login_password = request.POST.get('login_password','')
	
	if len(login_email) == 0:
		return HttpResponse("error,You forgot to enter an email address!")
	elif len(login_password) == 0:
		return HttpResponse("error,You forgot to enter a password!")
	
	user = User.objects.authenticate(email=login_email, password=login_password)
	
	if request.POST.get('remember_me','false') == "true":
		request.session.set_expiry(3600*24*30)
	else:
		request.session.set_expiry(0)
	
	if user is None:
		return HttpResponse("error,The email or password you entered was incorrect!")
	
	auth.login(request, user)
	
	return HttpResponse("valid")

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('index'))

@post_required()
@anonymous_required()
def register(request):
	signup_name = request.POST.get('signup_name','')
	signup_email = request.POST.get('signup_email','')
	signup_password = request.POST.get('signup_password','')
	
	try:
		User.objects.create_user(signup_name, signup_email, signup_password)
	except ValueError as e:
		return HttpResponse('error,' + str(e))
	
	newRequest = HttpRequest()
	newRequest.session = request.session
	newRequest.method = "POST"
	newRequest.POST['login_email'] = signup_email
	newRequest.POST['login_password'] = signup_password
	
	return login(newRequest)
