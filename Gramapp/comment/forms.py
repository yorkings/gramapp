from django.contrib.auth.models import User
from comment.models import Comment
from django import forms
from gram.models import Post

class NewCommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Write comment'}), required=True)
    post_id = forms.UUIDField(widget=forms.HiddenInput())  # Add the post_id field as a UUIDField

    class Meta:
        model = Comment
        fields = ("body", "post_id")  # Include the post_id field in the form
