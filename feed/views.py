from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect, get_object_or_404
import random
from .models import Profile, Post, Friend,Like_post,Room,Message,User_Room
from .utils.friend import make_friend, confirm_friend, delete_friend
from .utils.like import like_post
from django.http import JsonResponse,HttpResponse
import threading

# Create your views here.

def signup_view(request):
    context = {

    }
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cf_password = request.POST['cf_password']
        if password == cf_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, "user with that email already exists")
                return redirect('/signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "User with that username already exists")
            else:
                user = User.objects.create_user(email=email, password=password, username=username)
                user.save()

                #         this is how we create the profile for the user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                redirect('/')



        else:
            messages.info(request, 'Password does not match')
            return redirect('/signup')

    return render(request, 'feed/signup.html', context)


@login_required(login_url="/login")
def homepage_view(request):
    
    user_profile = Profile.objects.get(user=request.user)
    user_post = Post.objects.filter(user=request.user)
    
    len_post = len(user_post)
    
    friends=Friend.objects.all()
    posts_list=list()
    posts=list()
    for friend in friends:

        posts.append(Post.objects.filter(user = friend.friend_username).order_by('-createdAt'))
        posts.append(Post.objects.filter(user = friend.user.username).order_by('-createdAt'))
        posts.append(Post.objects.filter(user=request.user.username).order_by('-createdAt'))


    friend_requests = Friend.objects.filter(is_complete=False, user=request.user)
    for post in posts:
        for semi_post in post:
            posts_list.append(semi_post)

    like=Like_post.objects.filter(username=request.user)
    friends=list()
    frnd_possblty_1=Friend.objects.filter(sender_profile=Profile.objects.get(user=request.user))
    frnd_possblty_2=Friend.objects.filter(receiver_profile=Profile.objects.get(user=request.user))
    if frnd_possblty_1:
        for friend in frnd_possblty_1:
            friends.append(friend)
    if frnd_possblty_2:
        for friend in frnd_possblty_2:
            friends.append(friend)
    print(friends)
    context = {
        "user": user_profile.user,
        "profile": user_profile,
        "posts": posts_list,
        "friend_request": friend_requests,
        "len_friend_request": int(len(friend_requests)),
        "len_post":len_post,
        "len_like":int(len(like)),
        "friends":friends[:4],
        "len_friends":len(friends)
    }

    if request.method == 'POST':
        if request.FILES.get('post_img') is None:
            caption = request.POST['caption']
            user = user_profile.user
            Post.objects.create(caption=caption, user=user.username, profile=Profile.objects.get(user=request.user))

        if request.FILES.get('post_img'):
            image = request.FILES.get('post_img')
            caption = request.POST['caption']
            user = user_profile.user
            Post.objects.create(caption=caption, user=user.username, image=image,
                                profile=Profile.objects.get(user=request.user))
            print(image)

    return render(request, 'feed/homepage.html', context)


def login_view(request):
    context = {

    }
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            return redirect('/')
        else:
            messages.info(request, "Invalid Credentials")
            return redirect('/login')

    return render(request, "feed/login.html", context)


@login_required(login_url="/login")
def logout(request):
    auth.logout(request)
    return redirect('/login')


@login_required(login_url="/login")
def setting_view(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {
        "user": user_profile.user,
        "profile": user_profile
    }
    if request.method == "POST":
        if request.FILES.get('profile') is None:
            profile_img = user_profile.profile
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile = profile_img
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('profile') is not None:
            profile_img = request.FILES.get('profile')
            print(profile_img)
            bio = request.POST['bio']
            location = request.POST['location']
            user_profile.profile = profile_img
            user_profile.bio = bio
            user_profile.location = location
            user_profile.user.username = request.POST['username']
            print(request.POST['username'])
            user_profile.user.email = request.POST['email']
            print(request.POST['email'])
            user_profile.save()

    return render(request, "feed/setting.html", context)


@login_required(login_url='/login')
def message_view(request,username):
    user_profile = Profile.objects.get(user=request.user)

    friends=list()
    frnd_possblty_1=Friend.objects.filter(sender_profile=Profile.objects.get(user=request.user))
    frnd_possblty_2=Friend.objects.filter(receiver_profile=Profile.objects.get(user=request.user))
    if frnd_possblty_1:
        for friend in frnd_possblty_1:
            friends.append(friend)
    if frnd_possblty_2:
        for friend in frnd_possblty_2:
            friends.append(friend)
    current_sender_friend=None
    current_receiver_friend=None
    current_room=None
    for friend in friends:
        if friend.sender_profile==Profile.objects.get(user=User.objects.get(username=username)) :
            current_sender_friend=friend
            
        if friend.receiver_profile==Profile.objects.get(user=User.objects.get(username=username)):
            current_receiver_friend=friend

   
        if Room.objects.filter(name__icontains=username):
          for rooms in Room.objects.filter(name__icontains=username):
            if rooms.name==username+"-"+request.user.username or rooms.name==request.user.username+"-"+username:
                if User_Room.objects.get(user=request.user,room=rooms):      
                    room=User_Room.objects.filter(user=request.user,room=rooms)

        if room:
            for room in room:
                current_room=room.room.name
              
               
        else:
            current_room=username+"-"+request.user.username

    
    
    
    
    
    

    


        
  
            
    
    context = {
        "user": user_profile.user,
        "profile": user_profile,
        "friends":friends,
        "username":username,
        "current_sender_friend":current_sender_friend,
        "current_receiver_friend":current_receiver_friend,
        "current_room":current_room,
        
        
        
    }

            
            
        
    return render(request, 'feed/message.html', context)


@login_required(login_url='/login')
def like_view(request):
    username = request.user.username

    post_id = request.GET.get('post_id')

    like_post(username, post_id)
    return redirect('/')


@login_required(login_url='/login')
def friend_view(request):
    friend_username = request.user.username

    username = request.GET.get('username')
    user = User.objects.get(username=username)
    make_friend(user, friend_username)
    return redirect(f'/profile/{username}')

@login_required(login_url='/login')
def profile_view(request, username):
    profile_username = User.objects.get(username=username)
    profile = Profile.objects.get(user=User.objects.get(username=username))
    user_profile = Profile.objects.get(user=profile_username)
    user_post = Post.objects.filter(user=profile_username)
    len_post = len(user_post)
    latest_post = None
    isOwner = False
    if profile_username == request.user:
        isOwner = True
    friends = Friend.objects.all()
    isFriend = False
    for friend in friends:

        if request.user.username == friend.friend_username or request.user.username == friend.user.username:
            isFriend = True
    if user_post:
        for post in user_post:
            latest_post = post
    context = {
        "user": request.user,
        "profile": profile,
        "profile_username": profile_username,
        "user_profile": user_profile,
        "user_post": user_post,
        "len_post": int(len_post),
        "latest_post": latest_post,
        "friends": int(user_profile.friends),
        "isOwner": isOwner,
        "is_friend": isFriend

    }
   
    return render(request, 'feed/profile.html', context)

@login_required(login_url='/login')
def confirm_friend_view(request):
    friend_username = request.GET.get('username')

    username = request.user.username

    confirm_friend(request.user, friend_username)
    return redirect(f'/profile/{username}')

@login_required(login_url='/login')
def delete_friend_view(request):
    username = request.user.username

    delete_friend(request.user)
    return redirect(f'/profile/{username}')

@login_required(login_url='/login')
def search_view(request):
    user_profile = Profile.objects.get(user=request.user)
    print(user_profile.profile)
    search = request.GET.get('search')
    user_objects = User.objects.filter(username__icontains=search)
    search_post=list()
    posts=Post.objects.filter(caption__icontains=search)
    print(posts)
    for post in posts:
        search_post.append(post)
    print(search_post)
        
    profile_objects = list()
    profile_object_list=list()
    for user_object in user_objects:
        user_object_profile = Profile.objects.filter(user=User.objects.get(username=user_object))
        if user_object_profile:
            profile_objects.append(user_object_profile)


    for profile in profile_objects:
        for profile in profile:
            profile_object_list.append(profile)
    friends = Friend.objects.all()
    isFriend = False
    for friend in friends:

        if request.user.username == friend.friend_username or request.user.username == friend.user.username:
            isFriend = True


    context = {
        "user": user_profile.user,
        "profile": user_profile,
        "search_profile": profile_object_list,
        "search_post":search_post,
        "is_user":False


    }
    return render(request, 'feed/search_page.html', context)
@login_required(login_url='/login')
def get_messages(request,username):
    room=None
    messages_list=list()
    if Room.objects.filter(name__icontains=username):
        for rooms in Room.objects.filter(name__icontains=username):
            if rooms.name==username+"-"+request.user.username or rooms.name==request.user.username+"-"+username:
                if User_Room.objects.get(user=request.user,room=rooms):      
                    room=User_Room.objects.filter(user=request.user,room=rooms)

    if room:
        for room in room:
            current_room=room.room.name
            print(current_room)
            if Message.objects.filter(room=Room.objects.get(name=current_room)):
                messages=Message.objects.filter(room=Room.objects.get(name=current_room))
                for message in messages:
                    messages_list.append({"value":message.value,"user":{"username":message.user.username},"sender":{"username":message.sender.username},"date":message.date})
    else:
        current_room=username+"-"+request.user.username
    
    return JsonResponse({"messages":list(messages_list)})
    


    
    
def send_message(request):
    if request.method =='POST':
        room=request.POST['room']
        
        value=request.POST['message']
        username=request.POST['username']

        
        if Room.objects.filter(name=room):
            Message.objects.create(value=value,room=Room.objects.get(name=room),user=User.objects.get(username=username),sender=request.user)
            # Message.objects.create(value=value,room=Room.objects.get(name=room),user=request.user,sender=User.objects.get(username=username))
            if User_Room.objects.filter(room=Room.objects.get(name=room),user=User.objects.get(username=username)):
                pass
            else:
                User_Room.objects.create(room=Room.objects.get(name=room),user=User.objects.get(username=username))
                User_Room.objects.create(room=Room.objects.get(name=room),user=request.user)

        else:
            Room.objects.create(name=room)
            Message.objects.create(value=value,room=Room.objects.get(name=room),user=User.objects.get(username=username),sender=request.user)
            # Message.objects.create(value=value,room=Room.objects.get(name=room),user=request.user,sender=User.objects.get(username=username))
            if User_Room.objects.filter(room=Room.objects.get(name=room),user=User.objects.get(username=username)):
                pass
            else:
                User_Room.objects.create(room=Room.objects.get(name=room),user=User.objects.get(username=username))
                User_Room.objects.create(room=Room.objects.get(name=room),user=request.user)
    return HttpResponse("Message sent successfully")
    