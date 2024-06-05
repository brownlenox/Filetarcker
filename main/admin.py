from django.contrib import admin
from . models import UserProfile

admin.site.site_header = 'FileTracker'


admin.site.register(UserProfile)
