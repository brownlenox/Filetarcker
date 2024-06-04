from django.urls import path
from main import views
from django.conf.urls.static import static
from Filtracker import settings

urlpatterns = [
    path('', views.index, name="index"),
]
