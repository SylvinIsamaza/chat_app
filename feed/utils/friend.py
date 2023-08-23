from ..models import Friend,Profile
from django.contrib.auth.models import User
def make_friend(user,friend_username):
    friend_exist=Friend.objects.filter(friend_username=friend_username).first()
    friend_user=User.objects.get(username=friend_username)
    if friend_exist:
        friend_exist.delete()
        new_profile=Profile.objects.get(user=user)
        new_profile.friends=new_profile.friends-1
        new_profile_2 = Profile.objects.get(user=friend_user)
        new_profile_2.friends = new_profile_2.friends - 1
        new_profile.save()
        new_profile_2.save()
    else:

        new_friend=Friend.objects.create(user=user,friend_username=friend_username,sender_profile=Profile.objects.get(user=User.objects.get(username=friend_username)),receiver_profile=Profile.objects.get(user=User.objects.get(username=user.username)))
        new_friend.save()



def confirm_friend(user,friend_username):
    friend_username=User.objects.get(username=friend_username)
    new_profile = Profile.objects.get(user=user)
    new_profile_2=Profile.objects.get(user=friend_username)
    print(new_profile_2)
    print(new_profile)
    new_profile_2.friends=new_profile_2.friends +1
    new_profile.friends = new_profile.friends + 1
    new_friend = Friend.objects.filter(user=user,sender_profile=Profile.objects.get(user=friend_username))
    for new_friend in new_friend:
            
        if new_friend:
            new_friend.is_complete=True
            new_friend.save()
    new_profile.save()
    new_profile_2.save()

def delete_friend(user):
    new_friend = Friend.objects.filter(user=user)
    new_friend.delete()
