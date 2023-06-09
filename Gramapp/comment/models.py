from django.db import models
from django.contrib.auth.models import User
from gram.models import Post
from django.db.models.signals import post_save, post_delete
from notification.models import Notification


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)


def user_comment_post(sender, instance, *args, **kwargs):
    comment = instance
    post = comment.post
    text_preview = comment.body[:90]
    sender = comment.user
    notify = Notification(post=post, sender=sender, user=post.user, text_preview=text_preview, notification_types=2)
    notify.save()


def user_del_comment_post(sender, instance, *args, **kwargs):
    comment = instance
    post = comment.post
    sender = comment.user
    notify = Notification.objects.filter(post=post, sender=sender, user=post.user, notification_types=2)
    notify.delete()


post_save.connect(user_comment_post, sender=Comment)
post_delete.connect(user_del_comment_post, sender=Comment)
