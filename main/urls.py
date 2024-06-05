from django.urls import path
from main import views
from django.conf.urls.static import static
from Filtracker import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('track_file/', views.track_file, name="track_file"),
]
