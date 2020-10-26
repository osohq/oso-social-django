from django.forms import ModelForm, ModelMultipleChoiceField
from django.db.models import Q
from .models import Post, Role, User, Permission


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["contents", "access_level", "created_by"]

    def __init__(self, *args, **kwargs):
        self.authorized_to_create_for = kwargs.pop("authorized_to_create_for")
        super().__init__(*args, **kwargs)

        self.fields["created_by"].queryset = User.objects.filter(
            id__in=self.authorized_to_create_for
        )


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ["name", "users"]


class PermissionForm(ModelForm):
    class Meta:
        model = Permission
        fields = ["action", "resource"]