from django.contrib import admin
from .models import Profile,Post,Like_post,Friend,Room,Message,User_Room,Comment,Saved_Post,Reply_Reply,Shared_Post,Notification,Activity

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like_post)
admin.site.register(Friend)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(User_Room)
admin.site.register(Comment)
admin.site.register(Saved_Post)
admin.site.register(Shared_Post)
admin.site.register(Reply_Reply)
admin.site.register(Notification)
admin.site.register(Activity)