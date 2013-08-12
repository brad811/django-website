from django.test import TestCase
from django.test.client import Client

from website import views

import re

"""
Missing tests:
	- Test is_logged_in function
	- Test that index function renders home.html if logged in
	- Test that index function renders index.html if not logged in
"""

class RegisterTest(TestCase):
	def test_empty_email(self):
		"""
		Attempt to register a user with no email address
		"""
		c = Client()
		response = c.post('/register/', {'signup_email': '', 'signup_password': '12345678', 'signup_name': 'Sample Person'})
		self.assertEqual(response.content, "error,You must enter an email address.")
	
	def test_invalid_email(self):
		"""
		Attempt to register a user with an invalid email address
		"""
		c = Client()
		response = c.post('/register/', {'signup_email': 'invalid.email', 'signup_password': '12345678', 'signup_name': 'Sample Person'})
		self.assertEqual(response.content, "error,The email address entered is invalid.")
	
	def test_email_already_registered(self):
		"""
		Attempt to register a user with an email address that is already registered
		"""
		c = Client()
		c.post('/register/', {'signup_email': 'valid.email@website.com', 'signup_password': '12345678', 'signup_name': 'Sample Person'})
		response = c.post('/register/', {'signup_email': 'valid.email@website.com', 'signup_password': '12345678', 'signup_name': 'Sample Person 2'})
		self.assertEqual(response.content, "error,The email address entered is already registered.")
	
	def test_short_password(self):
		"""
		Attempt to register a user with a password that is too short
		"""
		c = Client()
		response = c.post('/register/', {'signup_email': 'valid.email@website.com', 'signup_password': '1234567', 'signup_name': 'Sample Person'})
		self.assertEqual(response.content, "error,The password must be at least 8 characters.")
	
	def test_empty_name(self):
		"""
		Attempt to register a user with no name
		"""
		c = Client()
		response = c.post('/register/', {'signup_email': 'valid.email@website.com', 'signup_password': '12345678', 'signup_name': ''})
		self.assertEqual(response.content, "error,You must enter a name.")
	
	def test_valid_registration(self):
		"""
		Attempt to register a user with valid information
		"""
		c = Client()
		response = c.post('/register/', {'signup_email': 'valid.email@website.com', 'signup_password': '12345678', 'signup_name': 'Sample Person'})
		self.assertEqual(response.content, "valid")

class LoginValidationTest(TestCase):
	def test_wrong_password(self):
		"""
		Attempt to login with the incorrect password
		"""
		c = Client()
		c.post('/register/', {'signup_email': 'email@website.com', 'signup_password': '12345678', 'signup_name': 'Sample Person'})
		response = c.post('/login/', {'login_email': 'email@website.com', 'login_password': '1234567'})
		self.assertEqual(response.content, "error,The email or password you entered was incorrect!")
	
	def test_wrong_email(self):
		"""
		Attempt to login with the incorrect email
		"""
		c = Client()
		c.post('/register/', {'signup_email': 'email@website.com', 'signup_password': '12345678', 'signup_name': 'Sample Person'})
		response = c.post('/login/', {'login_email': 'wrong_email@website.com', 'login_password': '12345678'})
		self.assertEqual(response.content, "error,The email or password you entered was incorrect!")
	
	def test_empty_email(self):
		"""
		Attempt to login with the no email address
		"""
		c = Client()
		response = c.post('/login/', {'login_email': '', 'login_password': '12345678'})
		self.assertEqual(response.content, "error,You forgot to enter an email address!")
	
	def test_empty_password(self):
		"""
		Attempt to login with no password
		"""
		c = Client()
		response = c.post('/login/', {'login_email': 'email@website.com', 'login_password': ''})
		self.assertEqual(response.content, "error,You forgot to enter a password!")
	
	def test_valid_login(self):
		"""
		Attempt to login with valid credentials
		"""
		c = Client()
		c.post('/register/', {'signup_email': 'email@website.com', 'signup_password': '12345678', 'signup_name': 'Sample Person'})
		response = c.post('/login/', {'login_email': 'email@website.com', 'login_password': '12345678'})
		self.assertEqual(response.content, "valid")
	
class LogoutTest(TestCase):
	def test_logout_unsets_cookie(self):
		"""
		Make sure logging out removes the 'user' cookie
		"""
		c = Client()
		response = c.post('/logout/')
		self.assertEqual(str(response.client.cookies.items()[0]), "('user', <Morsel: user=''>)")
	
	def test_logout_redirects_to_index(self):
		"""
		Make sure logging out redirects to the index
		"""
		c = Client()
		response = c.post('/logout/')
		self.assertTrue(re.match(r'^.*Location: http://testserver/$', ', '.join("%s: %s" % item for item in response.items())))
	
	