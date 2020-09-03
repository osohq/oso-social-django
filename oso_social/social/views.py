from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.urls import reverse

from .models import Post
from .forms import PostForm

# Create your views here.

def list_posts(request):
    # Limit to 10 latest posts.
    posts = Post.objects.all().order_by('-created_at')[:10]

    return render(request, 'social/list.html', {'posts': posts})

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
