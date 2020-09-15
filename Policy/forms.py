
import logging
from django.forms import BaseFormSet
from django.forms.models import inlineformset_factory
from django.utils import timezone
from django import forms
from .models import PolicyStatus, PolicyTransactionType, PartnerRole, PartnerType, Product, Policy, BusinessPartner
import datetime
from .signals import new_policy


class InsuranceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(InsuranceForm, self).__init__(*args, **kwargs)
        self.fields['role'].initial = 3
        self.fields['bp_Type'].initial = 1

    class Meta:
        model = BusinessPartner
        fields = '__all__'

        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.HiddenInput(),
            'bp_Type': forms.HiddenInput()
        }


class AgentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)
        self.fields['role'].initial = 2
        self.fields['bp_Type'].initial = 2

    class Meta:
        model = BusinessPartner
        fields = '__all__'

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'DOB': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control inputDOB-agent', 'autocomplete': "off"}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.HiddenInput(),
            'bp_Type': forms.HiddenInput()
        }


class HolderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(HolderForm, self).__init__(*args, **kwargs)
        self.fields['role'].initial = 1
        self.fields['bp_Type'].initial = 2

    class Meta:
        model = BusinessPartner
        fields = '__all__'

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'DOB': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control inputDOB', 'autocomplete': "off"}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.HiddenInput(),
            'bp_Type': forms.HiddenInput()
        }


class PolicyForm(forms.ModelForm):

    def __init__(self,  *args, **kwargs):
        self.product_id = kwargs.pop('product_id')
        super(PolicyForm, self).__init__(*args, **kwargs)
        self.fields['product'].initial = self.product_id

    def save(self, *args, **kwargs):
        super(PolicyForm, self).save(*args, **kwargs)
        newPolicy = self.instance
        new_policy.send(sender=Policy,
                        policy=newPolicy,
                        holder=newPolicy.policy_holder,
                        insurance=newPolicy.insurance,
                        agent=newPolicy.agent,
                        product=newPolicy.product)

    class Meta:
        model = Policy
        fields = '__all__'

        widgets = {
            'insurance': forms.Select(attrs={'class': 'form-control'}),
            'agent': forms.Select(attrs={'class': 'form-control'}),

            'product': forms.HiddenInput(),
            'effective_date': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control inputEffectiveDate', 'autocomplete': "off"}),
            'period_of_cover': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': "off", 'required': False}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'})
        }


PolicyFormSet = inlineformset_factory(
    BusinessPartner,  # parent form
    Policy,  # inline-form
    fk_name='policy_holder',  # specify the foreign key that links both model
    form=PolicyForm,  # set a custom form for the inline form
    extra=1)  # how many inline-forms are sent to the template by default
