from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from django_oso.auth import authorize
from django_oso.oso import Oso

from .models import Post, Role
from .forms import PostForm, RoleForm

# Create your views here.


def list_posts(request):
    # Limit to 10 latest posts.
    posts = Post.objects.all().order_by("-created_at")[:100]

    authorized_posts = []
    for post in posts:
        try:
            authorize(request, post, action="read")
            can_delete = Oso.is_allowed(request.user, "delete", post)
            authorized_posts.append({"post": post, "can_delete": can_delete})
        except PermissionDenied:
            continue

    return render(request, "social/list.html", {"posts": authorized_posts})


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, current_user=request.user)
        post = form.save(commit=False)

        authorize(request, post, action="create")
        post.save()
        return HttpResponseRedirect(reverse("index"))
    elif request.method == "GET":
        form = PostForm(current_user=request.user)
        return render(request, "social/new_post.html", {"form": form})
    else:
        return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def delete_post(request):
    if request.method == "POST":
        current_user = request.user
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)
        authorize(request, post, action="delete")
        post.delete()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseNotAllowed(["POST"])

    #     form = PostForm(request.POST, current_user=request.user)
    #     post = form.save(commit=False)

    #     authorize(request, post, action="create")
    #     post.save()
    #     return HttpResponseRedirect(reverse("index"))
    # elif request.method == "GET":
    #     form = PostForm(current_user=request.user)
    #     return render(request, "social/new_post.html", {"form": form})
    # else:
    #     return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def new_role(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        role = form.save(commit=False)

        role.created_by = request.user
        role.save()

        return HttpResponseRedirect(reverse("index"))
    elif request.method == "GET":
        form = RoleForm()
        return render(request, "social/new_role.html", {"form": form})
    else:
        return HttpResponseNotAllowed(["GET", "POST"])
