from ..models import Like_post,Post
def like_post(username,post_id):
    post=Post.objects.get(id=post_id)
    like_filter=Like_post.objects.filter(post_id=post_id,username=username).first()
    if like_filter ==None:
        new_like=Like_post.objects.create(post_id=post_id,username=username)
        new_like.save()

        post.no_of_like=post.no_of_like+1
        post.save()
    else:
        like_filter.delete()
        post.no_of_like=post.no_of_like-1;
        post.save()