from rest_framework import serializers
from .models import PolicyStatus, PolicyTransactionType, PartnerRole, PartnerType, Product, Policy, BusinessPartner


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'


class BusinessPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartner
        fields = '__all__'


class NewPolicySerializer(serializers.ModelSerializer):
    holder_id = PolicySerializer(many=True)

    class Meta:
        model = BusinessPartner
        fields = ('id', 'first_name', 'last_name', 'full_name', 'DOB', 'company_name', 'registration_number',
                  'email', 'phone', 'role', 'bp_Type', 'holder_id')

    def create(self, validated_data):
        new_holder = validated_data.pop('holder_id')
        policy_holder = BusinessPartner.objects.create(**validated_data)
        for holder in new_holder:
            Policy.objects.create(
                policy_holder=policy_holder, **holder)
        return policy_holder
