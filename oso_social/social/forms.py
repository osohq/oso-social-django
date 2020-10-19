from django.forms import ModelForm, ModelMultipleChoiceField
from django.db.models import Q
from .models import Post, Role, User

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
        # TODO: do this with oso + partial eval
        users = self.current_user.role_set.filter(create=True).values_list("created_by")
        q = User.objects.filter(Q(id__in=users) | Q(id=self.current_user.id))

        self.fields["created_by"].queryset = q


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ["name", "read", "create", "write", "delete", "users"]
