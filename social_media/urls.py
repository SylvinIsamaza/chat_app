"""social_media URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from feed.views import signup_view, homepage_view, login_view, logout, setting_view,message_view,like_view,profile_view,friend_view,confirm_friend_view,delete_friend_view,search_view,get_messages,send_message,upload_post,upload_comment_view,get_comment_view,upload_reply,upload_reply_to_reply,get_replies,get_replies_of_replies,save,get_saved_post
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup_view, name='sign up'),
    path('login/', login_view, name='Login'),
    path('logout/', logout, name='Logout'),
    path('settings/', setting_view, name='Setting'),
    path('profile/<str:username>', profile_view, name='Profile'),
    path('like', like_view, name='Like'),
    path('confirm_friend/', confirm_friend_view, name='confirm friend'),
    path('delete_friend/', delete_friend_view, name='delete friend'),
    path('search/', search_view, name='search'),
    path('get_message/<str:username>', get_messages, name='Get messages'),
    path('send_message', send_message, name='Send messages'),
    path('upload_post', upload_post, name='Upload post'),
    path('comment', upload_comment_view, name='Upload Comment'),
    path('get_comment',get_comment_view,name="Get comment"),
    
    path('message/<str:username>', message_view, name='Message'),
    path('reply',upload_reply, name='Crete Reply'),
    path('get_reply',get_replies, name='get replies'),
    path('reply_to_reply',upload_reply_to_reply, name='Reply to reply'),
    path('get_reply_to_reply',get_replies_of_replies, name='get Reply to reply'),
    path('save',save,name="Save post"),
    path('add_friend/', friend_view, name='Add friend'),
    path('', homepage_view, name='homepage')

]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
