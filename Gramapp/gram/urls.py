from django.urls import path
from .views import *

urlpatterns=[
    path('create/',createpost,name='newpost'),
    path('post/<uuid:post_id>',Postdetail,name='post'),
    path('dashboard/',dashboard,name='dashboard'),
    path('',home,name='home')
   
]
