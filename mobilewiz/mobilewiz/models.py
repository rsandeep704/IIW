__author__ = 'sandeep'

from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    class Meta:
        managed = True

    user = models.ForeignKey(User)
    pub_date = models.DateTimeField()
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title
