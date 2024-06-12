from django.urls import path
from main import views
from django.conf.urls.static import static
from Filtracker import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.user_login, name="login"),
    path('track_file/', views.track_file, name="track_file"),
    path("logout/",views.logout_view , name="logout"),
    path('account/', views.account, name="account"),
    path('edit-profile/', views.editprofile, name="edit-profile"),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('projects/<int:pk>/comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
   
    path('projects/<int:pk>/comments/<int:comment_id>/reply/', views.add_reply, name='add_reply'),


    path('projects/<int:project_id>/comments/<int:comment_id>/replies/<int:reply_id>/edit/', views.edit_reply, name='edit_reply'),
    path('projects/<int:project_id>/comments/<int:comment_id>/replies/<int:reply_id>/delete/', views.delete_reply, name='delete_reply'),

    path('projects/create/', views.create_project, name='new_application'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/delete/', views.delete_project, name='delete_project'),
    path('profile/', views.update_profile, name='profile'),
    path('admin/profile/<int:user_id>/', views.admin_update_profile, name='admin_update_profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
