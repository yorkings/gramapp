from django.urls import path
from .views import *

urlpatterns=[
    path('create/',createpost,name='newpost'),
    path('post/<uuid:post_id>', PostDetail, name='post'),
    path('dashboard/',index,name='dashboard'),
    path('',home,name='home'),
    path('tag/<slug:tag_slug>', Tags, name='tags'),
    path('<uuid:post_id>/favourite', favourite, name='favourite'),
    path('comment/', notification, name='comment1'),
    
    path('like/<int:post_id>/', like, name='like'),

]

 