from django.db import models
from django.db.models.signals import post_save,post_delete
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
from notification.models import Notification
# Create your models here.

#to upload user files to a specific directory
def user_images(instance,filename):
    return  'user {0}/{1}'.format(instance.user.id,filename)

class Tag(models.Model):
    title=models.CharField(max_length=100,verbose_name='Tag')
    slug=models.SlugField(null=False,unique=True,default=uuid.uuid1)
    class Meta:
        verbose_name='Tag'
        verbose_name_plural='Tags'
    def get_absolute_url(self):
        return reverse('tags',args=[self.slug]) 
    
    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.slug)
        return super().save(*args,**kwargs)    

class Post(models.Model):
    id= models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    picture=models.ImageField(upload_to='user_images',verbose_name='Picture',null=True)
    caption=models.CharField(max_length=100000,verbose_name='caption') 
    created=models.DateTimeField(auto_now_add=True)  
    tags=models.ManyToManyField(Tag,related_name='Tags') 
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    likes=models.IntegerField(default=0)    
    def get_absolute_url(self):
        return reverse('post',args=[str(self.id)]) 
    def __str__(self):
        return self.caption

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")

    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification(post=post, sender=sender, user=post.user)
        notify.save()

    def user_unliked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notify = Notification.objects.filter(post=post, sender=sender, notification_types=1)
        notify.delete()    

class Follow(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name='follower')
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')

    def user_follow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following
        notify = Notification(sender=sender, user=following, notification_types=3)
        notify.save()

    def user_unfollow(sender, instance, *args, **kwargs):
        follow = instance
        sender = follow.follower
        following = follow.following
        notify = Notification.objects.filter(sender=sender, user=following, notification_types=3)
        notify.delete()

class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='streams_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField()

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.created, following=user)
            stream.save()

post_save.connect(Stream.add_post, sender=Post)

post_save.connect(Likes.user_liked_post, sender=Likes)
post_delete.connect(Likes.user_unliked_post, sender=Likes)

post_save.connect(Follow.user_follow, sender=Follow)
post_delete.connect(Follow.user_unfollow, sender=Follow)



class Reel(models.Model):
    title = models.CharField(max_length=100)
    video_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    
