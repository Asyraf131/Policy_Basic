from django.db import models

# Create your models here.
from Policy.signals import new_policy
from Policy.models import Policy, BusinessPartner
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


@receiver(new_policy)
def handle_new_policy(sender, **kwargs):
    policy = kwargs['policy']
    policy_holder = kwargs['holder']
    insurance = kwargs['insurance']
    agent = kwargs['agent']
    product = kwargs['product']

    print('\nNew policy has been created at ',
          (policy.created_date + datetime.timedelta(hours=8)).strftime('%d/%m/%Y %I:%M%p'))
    print('Details are as follows:- \n')
    print('\tPolicy Holder: ', policy_holder)
    print('\tProduct:- ', product)
    print('\tInsurance:- ', insurance)
    print('\tAgent:- ', agent, '\n')


@receiver(post_save, sender=BusinessPartner)
def handler_new_parter(sender, instance, created, **kwargs):

    print('\nNew business partner (', instance.role, ') has been created at',
          (instance.created_date + datetime.timedelta(hours=8)).strftime('%d/%m/%Y %I:%M%p'))
    print('Details are as follows:- \n')
    if instance.full_name:
        print('\tFull Name: ', instance.full_name)
        print('\tDate of Birth:- ', instance.DOB.strftime('%d/%m/%Y'))
    else:
        print('\tCompany Name: ', instance.company_name)
        print('\tRegistration Number:- ', instance.registration_number)
    print('\tEmail:- ', instance.email)
    print('\tMobile:- ', instance.full_name, '\n')
