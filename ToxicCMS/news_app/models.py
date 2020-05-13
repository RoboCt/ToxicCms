from django.contrib.auth.models import User
from django.db import models


class Feed(models.Model):
    date_created = models.DateTimeField(null=False, auto_now_add=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    content = models.TextField(null=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    # image = models.ImageField(upload_to="uploads/feed", null=True, blank=True)
    # likes
    # comments
