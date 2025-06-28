from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, default='avatars/default_avatar.png')
    bio = models.TextField(max_length=60, blank=True, null=True)
    city = models.CharField(default='Moscow', max_length=30)

    def __str__(self):
        return f'{self.user.username} Profile'
