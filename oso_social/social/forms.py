from django.forms import ModelForm, ModelMultipleChoiceField
from django.db.models import Q
from .models import Post, Role, User, Permission


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

        # TODO: do this with oso + partial eval, this is just re-implementing `allow(user, write, post)` in django orm manually.
        # allow(user, write, post) if post.created_by = user;
        # allow(user, action, post) if
        #   role = user.role_set.all() and
        #   role.created_by.id = post.created_by.id and
        #   permission = role.permissions.all() and
        #   permission.get_resource() = "post" and
        #   permission.get_action() = "write";
        # getting all the users current user can create posts for
        users = self.current_user.role_set.filter(
            permissions__resource=Permission.RESOURCE_POST,
            permissions__action=Permission.ACTION_CREATE,
        ).values_list("created_by")
        # OR clause to let the current user create posts for themselves too
        q = User.objects.filter(Q(id__in=users) | Q(id=self.current_user.id))

        self.fields["created_by"].queryset = q


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ["name", "users"]
