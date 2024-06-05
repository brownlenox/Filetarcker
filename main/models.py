import os.path
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db import models

def unique_image_name(instance, filename):
    name = uuid.uuid4()
    print(name)
    ext = filename.split(".")[-1]
    full_name = f"{name}.{ext}"
    # full_name = "%s.%s" % (name, ext)
    return os.path.join('accounts', full_name)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=unique_image_name, null=True, blank=True)

    def __str__(self):
        return self.user.username