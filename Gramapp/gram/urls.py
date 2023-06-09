from django.urls import path
from .views import *

urlpatterns=[
    path('create/',createpost,name='newpost'),
    path('post/<uuid:post_id>',PostDetail,name='post'),
    path('dashboard/',dashboard,name='dashboard'),
    path('',home,name='home'),
    path('tag/<slug:tag_slug>', Tags, name='tags'),
    path('<uuid:post_id>/like', like, name='like'),
    path('<uuid:post_id>/favourite', favourite, name='favourite'),
    path('reels/', reels, name='reels'),
]

 