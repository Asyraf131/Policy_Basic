from django.contrib import admin
from .models import PolicyStatus, PolicyTransactionType, PartnerRole, PartnerType, Product, Policy, BusinessPartner

# Register your models here.


# class ChoiceInline(admin.TabularInline):
#     model = BusinessPartner
#     fk_name = "policy_holder"


class BusinessPartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'role_id', 'first_name', 'last_name', 'full_name', 'DOB', 'company_name', 'registration_number',
                    'email', 'phone', 'created_date', 'updated_date', 'bp_Type_id')


# class PolicyAdmin(admin.ModelAdmin):
#     inlines = [ChoiceInline]


admin.site.register(PolicyStatus)
admin.site.register(PolicyTransactionType)
admin.site.register(PartnerRole)
admin.site.register(PartnerType)
admin.site.register(Product)
admin.site.register(Policy)
admin.site.register(BusinessPartner, BusinessPartnerAdmin)
