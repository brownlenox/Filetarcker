from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'Home.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def track_file(request):
    return render(request, 'Track file.html')