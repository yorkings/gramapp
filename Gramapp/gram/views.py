from .models import *
from django.contrib.auth.models import User
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import *
from .forms import *
def home(request):
   return render(request,'home.html',{'user':request.user}) 
def dashboard(request):
   return render(request,'index.html',{'user':request.user}) 

 
def createpost(request):
    user = request.user.id
   
    tags_obj = []
    
    if request.method == "POST":
        form = Postform(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tags')
            tag_list = list(tag_form.split(','))

            for tag in tag_list:
                ta, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(ta)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user=user)
            p.tags.set(tags_obj)
            p.save()
            return redirect('index')
    else:
        form = Postform()
    context = {
        'form': form
    }
    return render(request, 'create_post.html', context)

def Postdetail(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    return render(request,'details.html',{'post':post})

