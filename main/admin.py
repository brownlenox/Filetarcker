from django.contrib import admin
from . models import UserProfile, Project, Contractor, Notification

admin.site.site_header = 'FileTracker'



admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Contractor)
admin.site.register(Notification)
