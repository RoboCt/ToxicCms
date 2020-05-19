from django.contrib.auth.models import User
from django.db import models

from userprofile.models import Profile


class FriendsList(models.Model):
    person = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='person', null=False)
    friend = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend', null=False)
    status = models.IntegerField(default=0, null=False, blank=False)

    def __str__(self):
        return self.person.user.username + '_' + self.friend.user.username
