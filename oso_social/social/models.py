from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Post(models.Model):
    contents = models.CharField(max_length=140)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=('created_at',))]
