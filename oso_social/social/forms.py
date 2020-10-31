from django.forms import ModelForm, ModelMultipleChoiceField
from django.db.models import Q
from .models import Post, Role, User, Permission


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["contents", "access_level"]


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ["name", "users"]

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop("organization")
        super().__init__(*args, **kwargs)

        self.fields["users"].queryset = User.objects.filter(
            organization=self.organization
        )


class PermissionForm(ModelForm):
    class Meta:
        model = Permission
        fields = ["action", "resource"]