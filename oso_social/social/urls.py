from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    list_posts,
    list_roles,
    new_post,
    delete_post,
    new_role,
    delete_role,
    new_permission,
    delete_permission,
    me,
)


urlpatterns = [
    path("", list_posts, name="index"),
    path("new_post/", new_post, name="new_post"),
    path("delete_post/", delete_post, name="delete_post"),
    path("new_role/", new_role, name="new_role"),
    path("roles/", list_roles, name="list_roles"),
    path("roles/delete_role", delete_role, name="delete_role"),
    path("roles/<role_id>/new_permission/", new_permission, name="new_permission"),
    path(
        "roles/<role_id>/delete_permission/",
        delete_permission,
        name="delete_permission",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="social/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("me", me, name="me"),
]
