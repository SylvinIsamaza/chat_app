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
    no_of_comments=models.IntegerField(default=0)
    no_of_shares=models.IntegerField(default=0)
    

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
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver",default=None)
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender",default=None)
    
    def __str__(self):
        return self.user.username

class User_Room(models.Model):
    room=models.ForeignKey(Room,on_delete=models.CASCADE,blank=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=False)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    value=models.CharField(max_length=10000,blank=False,default=None)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,blank=False,default=None,related_name="posts")
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None,blank=False,related_name="User")
    
    
    def __str__(self):  
      return self.value 

class Reply(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    value=models.CharField(max_length=10000,blank=False,default=None)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,blank=False,default=None,related_name="reply_post")
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None,blank=False,related_name="reply_user")
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE,default=None)


class Reply_Reply(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    value=models.CharField(max_length=10000,blank=False,default=None)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,blank=False,default=None,related_name="replied_post")
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None,blank=False,related_name="replied_user")
    Reply=models.ForeignKey(Reply,on_delete=models.CASCADE,default=None)


class Saved_Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,blank=False,default=None,related_name="saved_post")
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None,blank=False,related_name="user_who_save_post")

class Shared_Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,blank=False,default=None,related_name="shared_post")
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None,blank=False,related_name="user_who_share_post")
    to=models.ForeignKey(User,on_delete=models.CASCADE,default=None,blank=False,related_name="shared_to_user")
    