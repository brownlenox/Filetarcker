from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, LoginForm, EditProfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile



# Create your views here.
@login_required

def index(request):
    return render(request, 'Home.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            # Display error messages for invalid form data
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {field}: {error}')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Bind POST data to the form
        if form.is_valid():  # Check if the form is valid
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to the home page after successful login
            else:
                # Display error message for invalid credentials
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            # Display error message for invalid form data
            messages.error(request, 'Invalid form data. Please correct the errors below.')
    else:
        form = LoginForm()  # Create an empty form for GET requests

    return render(request, 'login.html', {'form': form})

def track_file(request):
    return render(request, 'Track file.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def account(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return render(request, 'account.html')

    return render(request, 'account.html', {'user_profile': user_profile})


def editprofile(request):
    try:
        user_profile = request.user.userprofile  # Try to get existing UserProfile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)  # Create a new UserProfile if it doesn't exist

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            user_profile.profile_picture = form.cleaned_data['profile_picture']
            user_profile.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('account')
        else:
            messages.error(request, 'There was an error updating your profile. Please check the form.')
    else:
        form = EditProfileForm(instance=request.user, initial={'profile_picture': user_profile.profile_picture})

    return render(request, 'edit-profile.html', {'form': form})
