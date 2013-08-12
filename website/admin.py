from django.contrib import admin
from website.models import User

class UserAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'location')
	list_filter = ['location']

admin.site.register(User, UserAdmin)