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
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
