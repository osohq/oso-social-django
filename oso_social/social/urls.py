from django.urls import path
from django.contrib.auth import views as auth_views

from .views import list_posts, new_post, new_role

urlpatterns = [
    path("", list_posts, name="index"),
    path("new/", new_post, name="new_post"),
    path("new_role/", new_role, name="new_role"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="social/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
