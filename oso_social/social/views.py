from django.shortcuts import render
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from django_oso.auth import authorize, authorize_model
from django_oso.oso import Oso

from .models import Post, Role, Permission
from .forms import PostForm, RoleForm, PermissionForm


def list_posts(request):
    # Limit to 100 latest posts.
    authorized_posts = (
        Post.objects.all()
        .authorize(request, action="read")
        .order_by("-created_at")[:100]
    )

    posts = [
        {"post": post, "can_delete": Oso.is_allowed(request.user, "delete", post)}
        for post in authorized_posts
    ]

    return render(request, "social/list.html", {"posts": posts})


@login_required
def list_roles(request):
    roles = Role.objects.filter(created_by=request.user)
    return render(request, "social/roles.html", {"roles": roles})


@login_required
def new_post(request):
    # this_user is the user trying to create the post
    # we get the users they are allowed to create a post for
    # by getting all of this_user's roles that have the "create" permission,
    # and getting the "created_by" field off of those roles

    # Use constraint propagation to get a filter that specifies who this user is allowed to create posts for
    authorized_to_create_for = []
    filter = authorize_model(None, Post, actor=request.user, action="create")
    for constraint in filter.children:
        field, value = constraint
        if field == "created_by":
            authorized_to_create_for.append(value.id)

    if request.method == "POST":
        form = PostForm(request.POST, authorized_to_create_for=authorized_to_create_for)
        post = form.save(commit=False)

        authorize(request, post, action="create")
        post.save()
        return HttpResponseRedirect(reverse("index"))
    elif request.method == "GET":
        form = PostForm(authorized_to_create_for=authorized_to_create_for)
        return render(request, "social/new_post.html", {"form": form})
    else:
        return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def delete_post(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post = Post.objects.get(id=post_id)
        authorize(request, post, action="delete")
        post.delete()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseNotAllowed(["POST"])


@login_required
def new_role(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        role = form.save(commit=False)

        role.created_by = (
            request.user._wrapped if hasattr(request.user, "_wrapped") else request.user
        )

        authorize(request, role, action="create")
        role.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse("list_roles"))
    elif request.method == "GET":
        form = RoleForm()
        return render(request, "social/new_role.html", {"form": form})
    else:
        return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def delete_role(request):
    if request.method == "POST":
        role_id = request.POST.get("role_id")
        role = Role.objects.get(id=role_id)
        authorize(request, role, action="delete")
        role.delete()
        return HttpResponseRedirect(reverse("list_roles"))
    else:
        return HttpResponseNotAllowed(["POST"])


@login_required
def new_permission(request, role_id):
    if request.method == "POST":
        form = PermissionForm(request.POST)
        permission = form.save(commit=False)
        role = Role.objects.get(id=role_id)

        permission.role = role

        authorize(request, permission, action="create")
        permission.save()

        return HttpResponseRedirect(reverse("list_roles"))
    elif request.method == "GET":
        form = PermissionForm()
        return render(
            request, "social/new_permission.html", {"form": form, "role_id": role_id}
        )
    else:
        return HttpResponseNotAllowed(["GET", "POST"])


@login_required
def delete_permission(request, role_id):
    if request.method == "POST":
        permission_id = request.POST.get("permission_id")
        permission = Permission.objects.get(id=permission_id)
        role = Role.objects.get(id=role_id)
        authorize(request, permission, action="delete")
        permission.delete()
        return HttpResponseRedirect(reverse("list_roles"))
    else:
        return HttpResponseNotAllowed(["POST"])