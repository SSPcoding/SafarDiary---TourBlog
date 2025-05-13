from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=480)
    photo = models.ImageField(upload_to="photos/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)  # New bio field

    def __str__(self):
        return self.user.username


class BucketList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True) 
    tweets = models.ManyToManyField(Tweet, related_name="saved_by_users", blank=True)

    def __str__(self):
        return f"{self.user.username}'s Bucket List"