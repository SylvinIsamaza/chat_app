from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect, get_object_or_404
import random
from .models import Profile, Post, Friend,Like_post,Room,Message,User_Room,Comment,Saved_Post,Reply_Reply,Saved_Post,Shared_Post,Notification,Activity
from .utils.friend import make_friend, confirm_friend, delete_friend
from .utils.like import like_post
from django.http import JsonResponse,HttpResponse
import threading
from datetime import datetime,timedelta
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
    rooms=list()
    message_list=list()

    all_rooms=list()
    user_room=User_Room.objects.filter(user=request.user)
    for room in user_room:
        rooms.append(room.room)
    for room in rooms:
        friend_in_room=User_Room.objects.filter(room=room)
        for friend_room in friend_in_room:
            if friend_room.user!=request.user:
                
                messages=Message.objects.filter(room=friend_room.room).order_by('-date').first()
               
                message_values=messages

                    
                message_list.append({
                    "user":friend_room.user,
                    "profile":Profile.objects.get(user=friend_room.user),
                    "messages":message_values
                })
                all_rooms.append(friend_room)
        

    
   
    for friend in friends:

        posts.append(Post.objects.filter(user = friend.friend_username).order_by('-createdAt'))
        posts.append(Post.objects.filter(user = friend.user.username).order_by('-createdAt'))
        posts.append(Post.objects.filter(user=request.user.username).order_by('-createdAt'))

    
    friend_requests = Friend.objects.filter(is_complete=False, user=request.user)
    for post in posts:
        for semi_post in post:
            liked_by_list=list()
            like_lists=Like_post.objects.filter(post_id=semi_post.id)
            for like_list in like_lists:
               print(like_list)
               liked_by_list.append(like_list)
               
          
            
            posts_list.append({"id":semi_post.id,"user":semi_post.user,"profile":semi_post.profile,"image":semi_post.image,"caption":semi_post.caption,'createdAt':semi_post.createdAt,"no_of_like":semi_post.no_of_like,"no_of_comments":semi_post.no_of_comments,"no_of_shares":semi_post.no_of_shares,"liked_by":liked_by_list})
            # print({"id":semi_post.id,"user":semi_post.user,"profile":semi_post.profile,"image":semi_post.image,"caption":semi_post.caption,'createdAt':semi_post.createdAt,"no_of_like":semi_post.no_of_like,"no_of_comments":semi_post.no_of_comments,"no_of_shares":semi_post.no_of_shares,"liked_by":liked_by_list})
                    
            
            
            

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
        "len_friends":len(friends),
        "messages":message_list
        
    }



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
def setting_view(request,tab):
    user_profile = Profile.objects.get(user=request.user)
    saved=Saved_Post.objects.filter(user=request.user)
    activity_list=list()
    
    def check_date(date1):
        date1=datetime.strptime(str(date1)[:10], '%Y-%m-%d')
        date2=datetime.strptime(str(datetime.now())[:10], '%Y-%m-%d')
        delta=date2-date1
        if date2==date1:
            return 'Today'
        elif date1==date2-timedelta(days=1):
            return 'yesterday'
        else:
            return str(date1)[:10]
    activities=Activity.objects.filter(user=request.user)
    for activity in activities:
        if activity.post_id:
            activity_list.append({"value":activity.value,"post":Post.objects.get(id=activity.post_id),"date":check_date(activity.date),"user":activity.user})
    context = {
        "user": user_profile.user,
        "profile": user_profile,
        "tab":tab,
        "saved":saved,
        "activity":activity_list
        
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

    
    
    
    
    
    

    


        
  
        rooms=list()
    message_list=list()

    all_rooms=list()
    user_room=User_Room.objects.filter(user=request.user)
    for room in user_room:
        rooms.append(room.room)
    for room in rooms:
        friend_in_room=User_Room.objects.filter(room=room)
        for friend_room in friend_in_room:
            if friend_room.user!=request.user:
                
                messages=Message.objects.filter(room=friend_room.room).order_by('-date').first()
               
                message_values=messages

                
                message_list.append({
                    "user":friend_room.user,
                    "profile":Profile.objects.get(user=friend_room.user),
                    "messages":message_values
                })

                all_rooms.append(friend_room)
   
    for friend in friends:
        print(friend.sender_profile.user)   
        if friend.sender_profile==Profile.objects.get(user=User.objects.get(username=username)) :
            for message in message_list:
                if message['user']!=friend.sender_profile.user:
                    
                    message_list.append({
                            "user":friend.friend_username,
                            "profile":Profile.objects.get(user=User.objects.get(username=username)),
                            "messages":{
                                "value":"Be first to say Hi"
                            }
                        })
            
        if friend.receiver_profile==Profile.objects.get(user=User.objects.get(username=username)):
            print(friend.receiver_profile.user) 
            for message in message_list:
                    if message['user']!=friend.receiver_profile.user:
                        
                        message_list.append({
                                "user":friend.friend_username,
                                "profile":Profile.objects.get(user=User.objects.get(username=username)),
                                "messages":{
                                    "value":"Be first to say Hi"
                                }
                            })

        
    
    context = {
        "user": user_profile.user,
        "profile": user_profile,
        "friends":friends,
        "username":username,
        "current_sender_friend":current_sender_friend,
        "current_receiver_friend":current_receiver_friend,
        "current_room":current_room,
        "messages":message_list
        
        
        
    }

            
            
        
    return render(request, 'feed/message.html', context)


@login_required(login_url='/login')
def like_view(request):
    username = request.user.username

    post_id = request.POST['post_id']

    like_post(request,username, post_id)
    post_like=Post.objects.get(id=post_id)

    return HttpResponse(post_like.no_of_like)


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
            if friend.is_complete:
                isFriend = True
            else:
                isFriend="pending"
        else:
            isFriend=False
                
    if user_post:
        for post in user_post:
            latest_post = post
    print(isFriend)
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
    


    
@login_required(login_url='/login')  
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
@login_required(login_url='/login') 
def upload_post(request):
    user_profile = Profile.objects.get(user=request.user)
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
    return HttpResponse("post uploaded successfully")
@login_required(login_url='/login') 
def upload_comment_view(request):
    if request.method == 'POST':
        comment=request.POST.get('comment')
        
        print(comment)
        
        post_id=request.POST['post_id']
        print(post_id)
        Comment.objects.create(value=comment,post=Post.objects.get(id=post_id),user=request.user)
        
        post=Post.objects.get(id=post_id)
        post.no_of_comments=post.no_of_comments+1
        post.save()
        
    return HttpResponse(post.no_of_comments)
@login_required(login_url='/login') 
def get_comment_view(request):
    comment_list=list()
    if request.method == 'GET':
        post_id=request.GET.get('post_id')
        print(post_id)
        comments=Comment.objects.filter(post=Post.objects.get(id=post_id))
        for comment in comments:
            comment_list.append({"id":comment.id,"value":comment.value,"post":{
                "id":comment.post.id,
                "user":comment.post.user,
            
                
            },"user":{
                "username":comment.user.username,
                "profile":Profile.objects.get(user=comment.user).profile.url
            }})
  
        
        
    return JsonResponse({"comment":comment_list})
        
@login_required(login_url='/login')        
def upload_reply(request):
    reply_list=list()
    if request.method=='POST':
        value=request.POST['value']
        comment_id=request.POST['comment_id']
        user=request.user,
        post_id=request.POST['post_id']
        
        Saved_Post.objects.create(user=user,post=Post.objects.get(id=post_id),value=value,comment=Comment.objects.get(id=comment_id))
        replies=Saved_Post.objects.filtet(comment=Comment.objects.get(id=comment_id))
        
        post=Post.objects.get(id=post_id)
        post.no_of_comments=post.no_of_comments+1
        post.save()
        for reply in replies:
            reply_list.append({"value":reply.value,"user":{"username":reply.user.username},"comment":{"id":reply.comment.id},"post":{"id":reply.post.id},"profile":Profile.objects.get(user=reply.user)})
    return JsonResponse({"replies":reply_list})

@login_required(login_url='/login') 
def delete_comment(request):
    id=request.GET['comment_id']
    comment=Comment.objects.get(id=id)
    post=comment.post
    post.no_of_comments=post.no_of_comments-1
    post.save()
    comment.delete()
   

    return HttpResponse(post.no_of_comments)

@login_required(login_url='/login')    
def get_replies(request):
    reply_list=list()
    
    if request.method=="GET":
        comment_id=request.GET['comment_id']
        
        
        replies=Saved_Post.objects.filtet(comment=Comment.objects.get(id=comment_id))
        print(replies)
        for reply in replies:
            reply_list.append({"value":reply.value,"user":{"username":reply.user.username},"comment":{"id":reply.comment.id},"post":{"id":reply.post.id},"profile":Profile.objects.get(user=reply.user)})
    return JsonResponse({"replies":reply_list})

@login_required(login_url='/login') 
def upload_reply_to_reply(request):
    if request.method == "POST":
        reply_id = request.POST.get('reply_id')
        value=request.POST.get('value')
        user=request.user,
        post_id=request.POST.get('post_id')
    
        Reply_Reply.objects.create(user=user,reply=Saved_Post.objects.get(id=reply_id),value=value,post=Post.objects.get(id=post_id))

        post=Post.objects.get(id=post_id)
        post.no_of_comments=post.no_of_comments+1
        post.save()
def get_replies_of_replies(request):
    reply_list=list()
    
    if request.method=="GET":
        reply_id=request.GET['reply_id']
        
        
        replies=Reply_Reply.objects.filtet(reply=Saved_Post.objects.get(id=reply_id))
        print(replies)
        for reply in replies:
            reply_list.append({"value":reply.value,"user":{"username":reply.user.username},"reply":{"id":reply.reply.id},"post":{"id":reply.post.id},"profile":Profile.objects.get(user=reply.user)})
    return JsonResponse({"replies":reply_list})

@login_required(login_url='/login') 
def save(request):
    saved_list=list()
    if request.method=='POST':
        user=request.user,
        post_id=request.POST['post_id']
        post_already_exist=Saved_Post.objects.filter(post=Post.objects.get(id=post_id),user=request.user)
        if not post_already_exist:
        
            Saved_Post.objects.create(user=request.user,post=Post.objects.get(id=post_id))
            saved_posts=Saved_Post.objects.filter(post=Post.objects.get(id=post_id))
            print(saved_posts)  
            for saved_post in saved_posts:
                saved_list.append({"user":{"username":saved_post.user.username},"post":{"id":saved_post.post.id},"profile":Profile.objects.get(user=saved_post.user)})

            return HttpResponse("saved successfully")
        else:
            return HttpResponse("Post already exists")
@login_required(login_url='/login') 
def get_saved_post(request):
    saved_list=list()
    
    if request.method=="GET":
        post_id=request.GET['post_id']
        
        
    
    saved_posts=Saved_Post.objects.filtet(post=Post.objects.get(id=post_id))
    print(saved_posts)
    for saved_post in saved_posts:
        saved_list.append({"user":{"username":saved_post.user.username},"post":{"id":saved_post.post.id},"profile":Profile.objects.get(user=saved_post.user)})
    return JsonResponse({"saved":saved_list})
@login_required(login_url='/login') 
def share(request):
    shared_list=list()
    if request.method=='POST':
        print(request.POST)
        user=request.user,
        
        post_id=request.POST['post']
        # print(post_id)    
        
        # Shared_Post.objects.create(user=user,post=Post.objects.get(id=post_id))
        # shared_post=Shared_Post.objects.filtet(post=Post.objects.get(id=post_id))
        # print(shared_post)
        shared_post=list()
        post=Post.objects.get(id=post_id)
        post.no_of_shares=post.no_of_shares+1
        post.save()
        for shared_post in shared_post:
            shared_list.append({"user":{"username":shared_post.user.username},"post":{"id":shared_post.post.id},"profile":Profile.objects.get(user=shared_post.user)})
        return JsonResponse({"saved":shared_list})
@login_required(login_url='/login') 
def get_shared_post(request):
    shared_list=list()
    
    if request.method=="GET":
        post_id=request.GET['post_id']
        
        
    
    shared_post=Shared_Post.objects.filtet(post=Post.objects.get(id=post_id))
    print(shared_post)

    for shared_post in shared_post:
        shared_list.append({"user":{"username":shared_post.user.username},"post":{"id":shared_post.post.id},"profile":Profile.objects.get(user=shared_post.user)})
    return JsonResponse({"saved":shared_list})

@login_required(login_url='/login') 
def message_page_view(request):
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
    print(friends)  
    context={
        'friends':friend,
        "profile":user_profile,
        "user":user_profile.user
    }
    return render(request,'feed/message_page.html',context)
@login_required(login_url='/login') 
def get_notification(request):
    notification_list=list()
    def check_date(date1):
        date1=datetime.strptime(str(date1)[:10], '%Y-%m-%d')
        date2=datetime.strptime(str(datetime.now())[:10], '%Y-%m-%d')
        delta=date2-date1
        if date2==date1:
            return 'Today'
        elif date1==date2-timedelta(days=1):
            return 'yesterday'
        else:
            return str(date1)[:10]
    
    user=request.user
    if request.method == 'GET':
        notifications=Notification.objects.filter(user=user).order_by('-date')
        for notification in notifications:
            
            print(notification.value)
            print(notification.date)
            print(datetime.now())
            print(notification.post)
            print(notification.viewed)
            profile=Profile.objects.get(user=User.objects.get(username=str(notification.value).split()[0]))    
            notification_list.append({
                "value":notification.value,
                "date":check_date(notification.date),
                "post":notification.post.id,
                "viewed":notification.viewed,
                "profile":{'user':profile.user.username,'image':profile.profile.url}
            })
            
            
       
    print(notification_list)
    
    return JsonResponse({"notification":notification_list})
        
        
@login_required(login_url='/login')    
def post_page(request,id):
    post=Post.objects.get(id=id)
    friends=list()
    frnd_possblty_1=Friend.objects.filter(sender_profile=Profile.objects.get(user=request.user))
    frnd_possblty_2=Friend.objects.filter(receiver_profile=Profile.objects.get(user=request.user))
    if frnd_possblty_1:
        for friend in frnd_possblty_1:
            friends.append(friend)
    if frnd_possblty_2:
        for friend in frnd_possblty_2:
            friends.append(friend)
    
    context={
        "post":post,
        "user":request.user,
        "profile":Profile.objects.get(user=request.user),
        "friends":friends
        
    }

    return render(request,'feed/post_page.html',context)