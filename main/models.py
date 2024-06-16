# models.py
import os.path
import uuid
from django.db import models
from django.contrib.auth.models import User

def unique_image_name(instance, filename):
    name = uuid.uuid4()
    ext = filename.split(".")[-1]
    full_name = f"{name}.{ext}"
    return os.path.join('accounts', full_name)

def unique_file_name(instance, filename):
    name = uuid.uuid4()
    ext = filename.split(".")[-1]
    full_name = f"{name}.{ext}"
    return os.path.join('projects', full_name)

class UserProfile(models.Model):
    USER_ROLES = (
        ('normal', 'Normal User'),
        ('officer', 'Handling Officer'),
        ('director', 'Director'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=unique_image_name, null=True, blank=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='normal')

    def __str__(self):
        return self.user.username

class Contractor(models.Model):
    name_of_contractor = models.CharField(max_length=100)

    def __str__(self):
        return self.name_of_contractor

class Project(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_of_the_project = models.CharField(max_length=100)
    project_type = models.CharField(max_length=100)
    tender_number = models.CharField(max_length=100)
    name_of_the_contractor = models.ForeignKey(Contractor, on_delete=models.SET_NULL, null=True, related_name='contractors')
    handling_officer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.name_of_the_project


class Notification(models.Model):

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    #recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    is_finished = models.BooleanField(default=False)
    message = models.TextField()
    is_read_by_handling_officer = models.BooleanField(default=False)
    is_read_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.project.name_of_the_project

class Comment(models.Model):
    project = models.ForeignKey(Project, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

