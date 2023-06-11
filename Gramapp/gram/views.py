from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Post, Tag, Follow, Stream, Likes
from django.contrib.auth.models import User
from .forms import Postform
from prof.models import Profile
from django.urls import resolve
from comment.models import Comment
from comment.forms import NewCommentForm
from django.core.paginator import Paginator
from .models import Reel
from django.db.models import Q
from gram.models import Post, Follow, Stream
from comment.forms import NewCommentForm
@login_required
def index(request):
    user = request.user
    user = request.user
    all_users = User.objects.all()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    profile = Profile.objects.all()

    posts = Stream.objects.filter(user=user)
        
    post_items = Post.objects.all().order_by('-created')
    context = {
        'poste': post_items,
        'follow_status': follow_status,
        'profile': profile,
        'all_users': all_users,
    }
    return render(request, 'dashboard.html', context)

@login_required
def createpost(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    tags_obj = []
    
    if request.method == "POST":
        form = Postform(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tags')
            tag_list = list(tag_form.split(','))

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user=user)
            p.tags.set(tags_obj)
            p.save()
            return redirect('profile', request.user.username)
    else:
        form = Postform()
    context = {
        'form': form
    }
    return render(request, 'create_post.html', context)

@login_required
def PostDetail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post', post_id=post_id)
    else:
        form = NewCommentForm()

    for comment in comments:
        profile = Profile.objects.get(user=comment.user)

    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, 'details.html', context)



@login_required
def Tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-created')

    context = {
        'posts': posts,
        'tag': tag

    }
    return render(request, 'tag.html', context)
@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
        
    post.likes = current_likes
    post.save()
    return HttpResponseRedirect(reverse('post', args=[post_id]))

@login_required
def favourite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('post', args=[post_id]))

def home(request):
   return render(request,'home.html',{'user':request.user}) 

@login_required
def dashboard(request):
   return render(request,'index.html',{'user':request.user}) 

def reels(request):
    reels = Reel.objects.all()
    return render(request, 'reels.html', {'reels': reels})




def messaging(request):
    return render(request, 'messaging.html')



  


def notification(request):
    user = request.user
    comments = Comment.objects.filter(post__user=user)
    context = {'comments': comments}
    return render(request, 'notification.html', context)

@login_required
def like(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    Likes.create_or_delete_like(user, post)
    liked = Likes.objects.filter(user=user, post=post).count()
    if liked % 2 == 0:
        Likes.objects.create(user=user, post=post)
        post.likes += 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        post.likes -= 1
    
    post.save()
    return HttpResponseRedirect(reverse('post', args=[post_id]))

