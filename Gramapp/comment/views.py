from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from gram.models import Post, Follow, Stream
from django.contrib.auth.models import User
from prof.models import Profile
from .forms import NewCommentForm
from django.urls import resolve
from .models import Comment
from datetime import datetime


# @require_POST
# def post_comment(request, post_id):
#     post = get_object_or_404(Post, id=post_id,)
#     comment = None

#     if request.method == 'POST':
#         form = NewCommentForm(data=request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#     else:
#         form = CommentForm()

#     comments = post.comments.filter(active=True)  # Retrieve all active comments for the post

#     return render(request, 'details.html', {'post': post, 'form': form,'comments': comments, 'comment': comment,})



 
def add_comment_to_post(request):
    form = NewCommentForm()

    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            post_id = form.cleaned_data['post_id']  # Assuming you have a field 'post_id' in the comment form
            try:
                post = Post.objects.all() # Retrieve the post based on the provided ID
            except Post.DoesNotExist:
                return render(request, 'error.html', {'message': 'Invalid post ID'})  # Handle invalid post ID

            comment = Comment(post=post, body=body)  # Assign the retrieved post to the comment
            comment.save()
            return redirect('comment')
        else:
            print('form is invalid')

    return render(request, 'comment.html', {'form': form})