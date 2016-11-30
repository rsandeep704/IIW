__author__ = 'sandeep'

from django.db import models
from django.contrib.auth.models import User
import uuid


class GlobalMobilePhoneModel(models.Model):
    class Meta:
        managed = True
        verbose_name = 'Mobile phone'
        verbose_name_plural = 'Mobile Phones'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256)
    brand = models.CharField(max_length=256)


class Companies(models.Model):
    class Meta:
        managed = True
        verbose_name = 'Mobile phone Selling Companies'
        verbose_name_plural = 'Mobile Phones Selling companies'

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)


class GlobalMobilePhones(models.Model):
    class Meta:
        managed = True
        verbose_name = "Mobile Phone"
        verbose_name_plural = "Mobile Phones"

    phone_model = models.ForeignKey(GlobalMobilePhoneModel)
    company = models.ForeignKey(Companies)
    totalCost = models.DecimalField(max_digits=10, decimal_places=2)
    emi = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_installments = models.IntegerField()


class GlobalSpecs(models.Model):
    class Meta:
        managed = True
        verbose_name = "Phone Specifications"

    pass


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

    class Meta:
        managed = True
        verbose_name = 'Data extracted from Verizon'

    def __str__(self):
        return self.name
