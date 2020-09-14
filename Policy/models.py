import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from django.urls import reverse
# Create your models here.


class BusinessPartner(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    DOB = models.DateField(null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    registration_number = models.CharField(
        max_length=255,  null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255)
    role = models.ForeignKey(
        'PartnerRole', on_delete=models.CASCADE, null=False, blank=True)
    bp_Type = models.ForeignKey(
        'PartnerType', on_delete=models.CASCADE, null=False, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.first_name:
            self.full_name = self.first_name + ' ' + self.last_name
        super().save(*args, **kwargs)

    def __str__(self):
        if self.first_name:
            return self.first_name + ' ' + self.last_name
        else:
            return self.company_name


class PartnerRole(models.Model):
    role_name = models.CharField(max_length=255)

    def __str__(self):
        return self.role_name


class PartnerType(models.Model):
    type_name = models.CharField(max_length=255)

    def __str__(self):
        return self.type_name


class Product(models.Model):
    product = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.product


class Policy(models.Model):
    insurance = models.ForeignKey(
        'BusinessPartner', on_delete=models.CASCADE, related_name='insurance_id',  limit_choices_to={'role_id': 3}, default=1)
    agent = models.ForeignKey(
        'BusinessPartner', on_delete=models.CASCADE, related_name='agent_id', limit_choices_to={'role_id': 2}, default=1)
    policy_holder = models.ForeignKey(
        'BusinessPartner', on_delete=models.CASCADE, related_name='holder_id', limit_choices_to={'role_id': 1}, default=1)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, null=False, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    effective_date = models.DateField()
    period_of_cover = models.DurationField(null=True, blank=True)
    status = models.ForeignKey(
        'PolicyStatus', on_delete=models.CASCADE, default=1)
    transaction_type = models.ForeignKey(
        'PolicyTransactionType', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.policy_holder.first_name + " " + self.policy_holder.last_name

    def save(self, *args, **kwargs):
        if self.period_of_cover:
            monthsToDays = self.period_of_cover.seconds * 30.436875
            self.period_of_cover = datetime.timedelta(days=monthsToDays)
        super().save(*args, **kwargs)


class PolicyStatus(models.Model):
    status_name = models.CharField(max_length=255)

    def __str__(self):
        return self.status_name


class PolicyTransactionType(models.Model):
    transaction_type = models.CharField(max_length=255)

    def __str__(self):
        return self.transaction_type
