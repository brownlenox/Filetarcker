from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegisterForm, LoginForm, EditProfileForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Reply, Notification
from .forms import (
    UserRegisterForm, LoginForm, EditProfileForm,
    UserProfileForm, UserProfileAdminForm, UserForm,
    ProjectForm, CommentForm
)
from .models import Project, Comment

def is_director(user):
    return user.is_superuser or (hasattr(user, 'userprofile') and user.userprofile.role == 'director')



# Create your views here.
@login_required

def index(request):
    return render(request, 'Home.html')

@login_required
def notifications(request):
    user = request.user
    user_profile = user.userprofile

    # Fetch unread notifications
    notifications = Notification.objects.filter(
        is_finished=False, 
        is_read_by_handling_officer=False, 
        project__handling_officer=user
    ).order_by('-project__created_at')
    
    notifications_finished = Notification.objects.filter(
        is_finished=True, 
        is_read_by_admin=False
    ).order_by('-project__created_at')
    
    display_notifications = list(notifications)
    display_notifications_finished = []

    # Admin/Director users see all 'project_finished' notifications
    if user.is_superuser or user_profile.role == 'director':
        display_notifications_finished = list(notifications_finished)

    return render(request, 'Notifications.html', {
        'display_notifications': display_notifications,
        'display_notifications_finished': display_notifications_finished,
    })
    
@login_required
def mark_project_finished(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user
    try:
            notification = Notification.objects.get(project=project)
            notification.is_finished = True
            notification.message = f"Project '{project.name_of_the_project}' by {project.handling_officer} is finished."
            notification.save()
    except Notification.DoesNotExist:
            # Handle the case where no notification exists for the project
            pass

        # Mark the project as finished (add your logic here)
            project.is_finished = True
            project.save()
          
       
    return redirect('project_list')

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    if request.user.is_superuser or request.user.userprofile.role == 'director':
        notification.is_read_by_admin = True
        notification.save()
    return redirect('notifications')

def accept_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    # Logic to handle accepting the project
    project.status = 'Accepted'
    project.save()
    # Update the related notification as read
    Notification.objects.filter(project=project).update(is_read_by_handling_officer=True,is_read_by_admin=False)
    return redirect('notifications')

def decline_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    # Logic to handle declining the project
    project.status = 'Declined'
    project.save()
    # Update the related notification as read
    Notification.objects.filter(project=project).update(is_read_by_handling_officer=True,is_read_by_admin=False)
    return redirect('notifications')   

   
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

@login_required
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

@login_required
@csrf_exempt
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


@login_required
def create_project(request):
    if request.method == 'POST':
        user = request.user
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = user
            project.save()

            notification = Notification(
                project=project,
                is_read_by_handling_officer = False
            )
            notification.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'new_application.html', {'form': form})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    comments = project.comments.all().order_by('-timestamp')


    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.project = project
            comment.save()
            return redirect('project_detail', pk=project.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'project_detail.html', {
        'project': project,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user.userprofile.role == 'director':
        if request.method == 'POST':
            project.delete()
            return redirect('project_list')
        return render(request, 'confirm_delete_project.html', {'project': project})
    else:
        return redirect('project_detail', pk=project_id)


@login_required
def edit_comment(request, pk, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'edit_comment.html', {'form': form})

@login_required
def delete_comment(request, pk, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    project = comment.project  # Retrieve the project associated with the comment
    if request.method == 'POST':
        comment.delete()
        return redirect('project_detail', pk=project.pk)
    return render(request, 'delete_comment.html', {'comment': comment, 'project': project})

@login_required
def add_reply(request, pk, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    project = comment.project
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.user = request.user
            reply.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ReplyForm()
    return render(request, 'add_reply.html', {'form': form, 'comment': comment, 'project': project})

@login_required
def edit_reply(request, project_id, comment_id, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user == reply.user:
        if request.method == 'POST':
            form = ReplyForm(request.POST, instance=reply)
            if form.is_valid():
                form.save()
                return redirect('project_detail', pk=project_id)
        else:
            form = ReplyForm(instance=reply)
        return render(request, 'edit_reply.html', {'form': form, 'reply': reply})
    else:
        return redirect('project_detail', pk=project_id)


@login_required
def delete_reply(request, project_id, comment_id, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user == reply.user:
        if request.method == 'POST':
            reply.delete()
            return redirect('project_detail', pk=project_id)
        return render(request, 'delete_reply.html', {'reply': reply})
    else:
        return redirect('project_detail', pk=project_id)



@login_required
def project_list(request):
    user = request.user
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'project_list.html', {
        'projects': projects,
        'userprofile': user.userprofile
    })


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
@user_passes_test(is_director)
def admin_update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileAdminForm(request.POST, request.FILES, instance=user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('admin_profile_list')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileAdminForm(instance=user.userprofile)
    
    return render(request, 'admin_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
