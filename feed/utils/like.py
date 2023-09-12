from django.contrib.auth.models import User
from ..models import Activity
from ..models import Like_post,Post,Notification
def like_post(request,username,post_id):
    post=Post.objects.get(id=post_id)
    like_filter=Like_post.objects.filter(post_id=post_id,username=username).first()
    if like_filter ==None:
        new_like=Like_post.objects.create(post_id=post_id,username=username)
        new_like.save()

        post.no_of_like=post.no_of_like+1
        post.save()
            
        user=User.objects.get(username=Post.objects.filter(id=post_id).first().user)
        if request.user.username!=User.objects.get(username=Post.objects.filter(id=post_id).first().user):
            
            Notification.objects.create(user=user,value=f"{username} Liked your post",post=Post.objects.get(id=post_id))
            Activity.objects.create(user=request.user,post_id=post_id,value=f'You liked post of {post.user}')
    else:
        like_filter.delete()
        post.no_of_like=post.no_of_like-1;
        post.save()