from django.shortcuts import render
from django.http import HttpResponse

from .models import Post

# Create your views here.

def list_posts(request):
    # Limit to 10 latest posts.
    posts = Post.objects.all()[:10]

    posts_text = ""

    for post in posts:
        posts_text += f"@{post.created_by} {post.contents}"

    return HttpResponse(posts_text)
