from django.contrib import admin
from .models import Profile,Post,Like_post,Friend,Room,Message

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like_post)
admin.site.register(Friend)
admin.site.register(Room)
admin.site.register(Message)
