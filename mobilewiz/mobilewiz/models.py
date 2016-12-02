__author__ = 'sandeep'

from django.db import models
from django.contrib.auth.models import User
import uuid


class GlobalMobilePhoneModel(models.Model):
    class Meta:
        managed = True
        verbose_name = 'Mobile phone Model'
        verbose_name_plural = 'Mobile Phone Models'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256)
    modelName = models.CharField(max_length=256)

    def __str__(self):
        return self.modelName

class GlobalMobilePhones(models.Model):
    class Meta:
        managed = True
        verbose_name = "Mobile Phone"
        verbose_name_plural = "Mobile Phones"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256)
    phone_model = models.ForeignKey(GlobalMobilePhoneModel)
    company = models.CharField(max_length=256)
    totalCost = models.DecimalField(max_digits=10, decimal_places=2)
    emi = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_installments = models.IntegerField()
    down_payment = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.URLField()
    imageUrl = models.URLField()

    def __str__(self):
        return self.title


class ATTData(models.Model):
    class Meta:
        managed = True
        verbose_name = 'Data extracted from AT&T'

    url = models.URLField()
    name = models.CharField(max_length=256)
    model = models.CharField(max_length=256)
    memory = models.CharField(max_length=256)
    sku_id = models.CharField(max_length=50)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    down_payment = models.DecimalField(max_digits=10, decimal_places=2)
    emi = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_installments = models.IntegerField()
    brand = models.CharField(max_length=256)
    imageUrl = models.URLField()

    def __str__(self):
        return self.name


class TMobileData(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=256)
    memory = models.CharField(max_length=256)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    down_payment = models.DecimalField(max_digits=10, decimal_places=2)
    emi = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_installments = models.IntegerField()
    brand = models.CharField(max_length=256)
    imageUrl = models.URLField()

    class Meta:
        managed = True
        verbose_name = 'Data extracted from TMobile'

    def __str__(self):
        return self.name


class VerizonData(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=256)
    memory = models.CharField(max_length=256)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    down_payment = models.DecimalField(max_digits=10, decimal_places=2)
    emi = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_installments = models.IntegerField()
    brand = models.CharField(max_length=256)
    imageUrl = models.URLField()

    class Meta:
        managed = True
        verbose_name = 'Data extracted from Verizon'

    def __str__(self):
        return self.name
