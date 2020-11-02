from django.db import models

from django.contrib.auth.models import AbstractUser

from django_oso.models import AuthorizedModel


class Organization(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=1)


class Post(AuthorizedModel):
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

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        indexes = [models.Index(fields=("created_at",))]

    def __str__(self):
        if len(self.contents) > 20:
            return f'{self.created_by.username} | "{self.contents[:20]}..."'
        else:
            return f'{self.created_by.username} | "{self.contents}"'


class Role(AuthorizedModel):
    name = models.CharField(max_length=140)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    custom = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    users = models.ManyToManyField(User)

    def __str__(self):
        return f"{self.name} for {self.organization.name}"


class Permission(AuthorizedModel):
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
    RESOURCES = [(RESOURCE_POST, "post")]

    action = models.IntegerField(choices=ACTIONS)
    resource = models.IntegerField(choices=RESOURCES)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions")

    def get_action(self):
        return dict(self.ACTIONS)[self.action]

    def get_resource_kind(self):
        return dict(self.RESOURCES)[self.resource]

    def __str__(self):
        return f"{self.role} | {self.get_action()} on {self.get_resource_kind()}"
