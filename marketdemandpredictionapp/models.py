from django.contrib.auth.models import User
from django.db import models


class Crops(models.Model):

    crop_name = models.CharField(max_length=100)
    crop_code = models.PositiveIntegerField()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f"Username: {self.user.username}"


