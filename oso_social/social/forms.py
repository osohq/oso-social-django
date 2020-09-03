from django.forms import ModelForm

from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['contents', 'access_level']
