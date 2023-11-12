from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Crops(models.Model):

    crop_name = models.CharField(max_length=100)
    crop_code = models.PositiveIntegerField()
    crop_description = models.CharField(max_length=10000)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f"Username: {self.user.username}"

class UserPreferences(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, db_column='user_profile_id')
    selected_crop = models.ForeignKey(Crops, on_delete=models.CASCADE, db_column='selected_crop_id')
    selected_start_year = models.IntegerField(null=True)
    selected_end_year = models.IntegerField()
    request_time = models.DateTimeField(default=datetime.now, blank=False)
    def __str__(self):
        return self.user.username

