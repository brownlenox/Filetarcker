from django.contrib import admin
from . models import UserProfile, Project

admin.site.site_header = 'FileTracker'



admin.site.register(UserProfile)
admin.site.register(Project)
