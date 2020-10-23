from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Post(models.Model):
    ACCESS_PUBLIC = 0
    ACCESS_PRIVATE = 1
    ACCESS_LEVEL_CHOICES = [
        (ACCESS_PUBLIC, "Public"),
        (ACCESS_PRIVATE, "Private"),
    ]

    contents = models.CharField(max_length=140)

    access_level = models.IntegerField(
        choices=ACCESS_LEVEL_CHOICES, default=ACCESS_PUBLIC
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=("created_at",))]


class Role(models.Model):
    name = models.CharField(max_length=140)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_role_created",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    users = models.ManyToManyField(User)


class Permission(models.Model):
    ACTION_READ = 0
    ACTION_CREATE = 1
    ACTION_UPDATE = 2
    ACTION_DELETE = 3
    ACTIONS = [
        (ACTION_READ, "read"),
        (ACTION_CREATE, "create"),
        (ACTION_UPDATE, "update"),
        (ACTION_DELETE, "delete"),
    ]

    RESOURCE_POST = 0
    RESOURCE_ROLE = 1
    RESOURCES = [(RESOURCE_POST, "post"), (RESOURCE_ROLE, "role")]

    action = models.IntegerField(choices=ACTIONS)
    resource = models.IntegerField(choices=RESOURCES)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions")

    def get_action(self):
        return dict(self.ACTIONS)[self.action]

    def get_resource(self):
        return dict(self.RESOURCES)[self.resource]
