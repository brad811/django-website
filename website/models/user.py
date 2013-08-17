from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, check_password
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist

class UserManager(BaseUserManager):
	def create_user(self, name, email, password):
		"""
		Creates and saves a User with the given name, email,
		and password.
		"""
		if not name:
			raise ValueError('You forgot to enter a name!')
		if not email:
			raise ValueError('You forgot to enter an email address!')
		if not password:
			raise ValueError('You forgot to enter a password!')
		try:
			validate_email(email)
		except ValidationError:
			raise ValueError('The email address entered is invalid.')
		if User.objects.filter(email=email).count() > 0:
			raise ValueError('The email address entered is already registered.')
		if len(password) < 8:
			raise ValueError('The password must be at least 8 characters.')
		
		user = self.model(
			name=name,
			email=self.normalize_email(email),
		)
		
		user.set_password(password)
		user.save(using=self._db)
		return user
	
	def authenticate(self, email, password):
		"""
		Authenticate a user based on email address as the user name.
		"""
		try:
			user = User.objects.get(email=email)
			if user.check_password(password):
				user.backend = 'django.contrib.auth.backends.ModelBackend'
				return user
			else:
				return None
		except User.DoesNotExist:
			return None

class User(AbstractBaseUser):
	email = models.EmailField(max_length=254, unique=True)
	name = models.CharField(max_length=80)
	location = models.CharField(max_length=60)
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['email', 'password', 'name']
	
	objects = UserManager()
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		app_label = 'website'

		