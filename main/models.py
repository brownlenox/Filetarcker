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

class Project(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    contractor = models.CharField(max_length=100)
    handling_officer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projects')
    contract_type = models.CharField(max_length=50)
    files = models.FileField(upload_to=unique_file_name, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

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

