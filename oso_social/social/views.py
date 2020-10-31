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
    authorized_posts = []
    for post in Post.objects.all().order_by("-created_at")[:100]:
        try:
            authorize(request, action="read", resource=post)
        except:
            continue
        authorized_posts.append(
            {"post": post, "can_delete": Oso.is_allowed(request.user, "delete", post)}
        )

    return render(request, "social/list.html", {"posts": authorized_posts})


@login_required
def list_roles(request):
    authorized_roles = []
    for role in Role.objects.all():
        try:
            authorize(request, action="read", resource=role)
        except:
            continue
        authorized_roles.append(role)

    return render(request, "social/roles.html", {"roles": authorized_roles})


@login_required
def new_post(request):

    if request.method == "POST":
        form = PostForm(request.POST)
        post = form.save(commit=False)
        post.created_by = (
            request.user._wrapped if hasattr(request.user, "_wrapped") else request.user
        )
        post.organization = request.user.organization

        authorize(request, post, action="create")
        post.save()
        return HttpResponseRedirect(reverse("index"))
    elif request.method == "GET":
        form = PostForm()
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
        form = RoleForm(request.POST, organization=request.user.organization)
        role = form.save(commit=False)

        role.created_by = (
            request.user._wrapped if hasattr(request.user, "_wrapped") else request.user
        )
        role.organization = request.user.organization

        authorize(request, role, action="create")
        role.save()
        form.save_m2m()
        return HttpResponseRedirect(reverse("list_roles"))
    elif request.method == "GET":
        form = RoleForm(organization=request.user.organization)
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


@login_required
def me(request):
    return render(request, "social/me.html", {"me": request.user})


def oso_context_processor(request):
    """Pass authZ context into templates."""
    is_moderator = Oso.is_allowed(request.user, "GET", "roles")
    return {"is_moderator": is_moderator}