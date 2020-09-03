from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from django_oso.auth import authorize

from .models import Post
from .forms import PostForm

# Create your views here.

def list_posts(request):
    # Limit to 20 latest posts.
    posts = Post.objects.all().order_by('-created_at')[:20]

    authorized_posts = []
    for post in posts:
        try:
            # TODO (dhatch): This is an issue with the authorize interface!
            authorize(request, post, action="view")
            authorized_posts.append(post)
        except PermissionDenied:
            continue

    return render(request, 'social/list.html', {'posts': authorized_posts})

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        post = form.save(commit=False)

        post.created_by = request.user
        post.save()

        return HttpResponseRedirect(reverse('index'))
    elif request.method == 'GET':
        form = PostForm()
        return render(request, 'social/new_post.html', { 'form': form })
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
