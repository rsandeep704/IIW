__author__ = 'sandeep'

from django.db import models
from django.contrib.auth.models import User
import uuid


class Note(models.Model):
    class Meta:
        managed = True

    user = models.ForeignKey(User)
    pub_date = models.DateTimeField()
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title


class GlobalTable(models.Model):
    class Meta:
        managed = True

    mobileID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    descriptionLink = models.TextField()
    # atnt = models.ForeignKey(ATnT)
    # tMobile = models.ForeignKey(TMobile)
    # verizon = models.ForeignKey(Verizon)
    pmoCost = models.DecimalField(max_digits=10,decimal_places=2)
    company = models.CharField(max_length=200)
    totalCost = models.DecimalField(max_digits=10,decimal_places=2)
    link = models.TextField()

    def __str__(self):
        return self.name


# class ATnT(models.Model):
#     class Meta:
#         manged = True
#
#     name = models.CharField(max_length=200)
#     pmoCost = models.DecimalField()
#
#
# class TMobile(models.Model):
#     class Meta:
#         manged = True
#
#
# class Verizon(models.Model):
#     class Meta:
#       manged = True


