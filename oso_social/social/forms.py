from django.forms import ModelForm, ModelMultipleChoiceField
from django.db.models import Q
from .models import Post, Role, User, Permission

from django_oso.oso import Oso


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["contents", "access_level", "created_by"]

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("current_user")
        super().__init__(*args, **kwargs)

        # this_user is the user trying to create the post
        # q is the query set of users that this user is allowed to create posts for
        # we get q by getting all of this_user's roles that have the "create" permission, and getting the "created_by"
        # field off of those roles

        # TODO: do this with oso + partial eval, where you can just pass in the post partial
        users = User.objects.all()

        authorized_to_create_for = [self.current_user.id]
        for user in users:
            if list(
                Oso.query_rule(
                    "allow_by_model",
                    self.current_user,
                    "create",
                    {"type": "post", "owner": user},
                )
            ):
                authorized_to_create_for.append(user.id)
        print(authorized_to_create_for)

        self.fields["created_by"].queryset = User.objects.filter(
            id__in=authorized_to_create_for
        )


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ["name", "users"]


class PermissionForm(ModelForm):
    class Meta:
        model = Permission
        fields = ["action", "resource"]