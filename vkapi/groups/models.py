from django.db import models
from django.contrib.auth.models import User

class Credential(models.Model):
    user = models.OneToOneField(User, null=True, related_name='credentials')
    client_id = models.CharField(max_length=20, blank=True)
    account_id = models.CharField(max_length=20, blank=True)
    token = models.CharField(max_length=50, blank=True)
    secret = models.CharField(max_length=50, blank=True)
    url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.user.get_full_name()