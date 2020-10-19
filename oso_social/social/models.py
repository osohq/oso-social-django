from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Post(models.Model):
    ACCESS_PUBLIC = 0
    ACCESS_PRIVATE = 1
    ACCESS_LEVEL_CHOICES = [
        (ACCESS_PUBLIC, 'Public'),
        (ACCESS_PRIVATE, 'Private'),
    ]

    contents = models.CharField(max_length=140)

    access_level = models.IntegerField(choices=ACCESS_LEVEL_CHOICES, default=ACCESS_PUBLIC)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=("created_at",))]


class Role(models.Model):
    name = models.CharField(max_length=140)

    read = models.BooleanField()
    create = models.BooleanField()
    write = models.BooleanField()
    delete = models.BooleanField()

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_role_created"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    users = models.ManyToManyField(User)
