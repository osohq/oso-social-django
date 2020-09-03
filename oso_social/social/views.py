from django.shortcuts import render

from .models import Post

# Create your views here.

def list_posts(request):
    # Limit to 10 latest posts.
    posts = Post.objects.all()[:10]

    return render(request, 'social/list.html', {'posts': posts})
