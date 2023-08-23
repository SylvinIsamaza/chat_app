from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.utils.timezone import timezone

User = get_user_model()


# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profile = models.ImageField(upload_to='profile_img', default="user.svg")
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=50, blank=True)
    friends = models.IntegerField(default=0, )

    def __str__(self):
        return self.user.username

    def clean_friends(self, exclude=None):
        if int(self.friends) >= 0:
            return self.friends
        else:
            return 0


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,default=None)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    createdAt = models.DateTimeField(default=datetime.now)
    no_of_like = models.IntegerField(default=0)
    comments = [models.TextField()]

    def __str__(self):
        return self.user


class Like_post(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=500)

    def __str__(self):
        return self.username


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    sender_profile=models.ForeignKey(Profile,on_delete=models.CASCADE,default=None,related_name='sent_friend_requests')
    receiver_profile=models.ForeignKey(Profile,on_delete=models.CASCADE,default=None,related_name="receiver_friend_request")
    is_complete = models.BooleanField(default=False)
    friend_username = models.CharField(max_length=500)

    def __str__(self):
        return self.friend_username


class Room(models.Model):
    name=models.CharField(max_length=500)
    
    
    def __str__(self):
        return self.name
class Message(models.Model):
    value=models.CharField(max_length=1000000)
    date=models.DateTimeField(default=datetime.now,blank=True)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.value
    