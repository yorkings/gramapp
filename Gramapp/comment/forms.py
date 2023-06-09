from django.contrib.auth.models import User
from comment.models import Comment
from django import forms
from gram.models import Post

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['user', 'post']
