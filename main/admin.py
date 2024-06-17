from django.contrib import admin
from .models import UserProfile, Project, Contractor, Notification

admin.site.site_header = 'FileTracker'

class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 1  # Number of extra forms to show

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'profile_picture')
    list_filter = ('role',)
    search_fields = ('user__username', 'role')

@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ('name_of_contractor',)
    search_fields = ('name_of_contractor',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name_of_the_project', 'user', 'project_type', 'tender_number',
        'name_of_the_contractor', 'handling_officer', 'status', 'is_finished', 'created_at'
    )
    list_filter = ('status', 'is_finished', 'created_at', 'handling_officer')
    search_fields = (
        'name_of_the_project', 'user__username', 'project_type',
        'tender_number', 'name_of_the_contractor__name_of_contractor'
    )
    list_editable = ('status', 'is_finished')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 20
    inlines = [NotificationInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'name_of_the_contractor', 'handling_officer')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('project', 'is_finished', 'message', 'is_read_by_handling_officer', 'is_read_by_admin')
    list_filter = ('is_finished', 'is_read_by_handling_officer', 'is_read_by_admin')
    search_fields = ('project__name_of_the_project', 'message')
    list_editable = ('is_finished', 'is_read_by_handling_officer', 'is_read_by_admin')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('project')

# Removing any previous registration attempts
# try:
#     admin.site.unregister(UserProfile)
#     admin.site.unregister(Project)
#     admin.site.unregister(Contractor)
#     admin.site.unregister(Notification)
# except admin.sites.NotRegistered:
#     pass

# Register the models with the admin site only once
# admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(Project, ProjectAdmin)
# admin.site.register(Contractor, ContractorAdmin)
# admin.site.register(Notification, NotificationAdmin)
