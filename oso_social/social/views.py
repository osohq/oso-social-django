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
    posts = (Post.objects.authorize(request, action="view")
        .select_related('created_by')
        .order_by('-created_at'))

    return render(request, 'social/list.html', {'posts': posts})

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
