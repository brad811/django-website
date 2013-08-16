from django.utils.functional import wraps
from django.utils.decorators import available_attrs
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect

from website.models import User

def request_passes_test(test_func):
	def decorator(view_func):
		@wraps(view_func, assigned=available_attrs(view_func))
		def _wrapped_view(request, *args, **kwargs):
			if test_func(request):
				return view_func(request, *args, **kwargs)
				
			return HttpResponseRedirect(reverse('index'))
		return _wrapped_view
	return decorator

def login_required():
	actual_decorator = request_passes_test(
		lambda request: get_user(request).is_authenticated()
	)
	return actual_decorator

def anonymous_required():
	actual_decorator = request_passes_test(
		lambda request: get_user(request).is_anonymous()
	)
	return actual_decorator

def post_required():
	actual_decorator = request_passes_test(
		lambda request: request.method == "POST"
	)
	return actual_decorator

def get_user(request):
	try:
		user = User.objects.get(pk=request.session.get('_auth_user_id'))
	except User.DoesNotExist:
		user = AnonymousUser()
	
	return user