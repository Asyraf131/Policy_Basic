from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import PolicyStatus, PolicyTransactionType, PartnerRole, PartnerType, Product, Policy, BusinessPartner
from django.db.models.functions import Concat
from django.db.models import F, Value
from django.db import connection
from itertools import chain
import datetime
from .forms import PolicyForm, PolicyFormSet, HolderForm, InsuranceForm, AgentForm
from django.views.generic import CreateView
from .signals import new_policy

# Create your views here.


class NavBar(View):
    def get(self, request):
        product = Product.objects.all()
        context = {'Products': product}
        return render(request, 'Policy/index.html', context)


class BusinessPartnerListView(View):
    def get(self, request):
        product = Product.objects.all()
        partners = BusinessPartner.objects.all().order_by('-id')
        context = {'BusinessPartners': partners, 'Products': product}

        return render(request, 'Policy/partnerList.html', context)


class BusinessPartnerDetailView(View):
    def get(self, request, pk, type):
        product = Product.objects.all()
        detail = BusinessPartner.objects.get(id=pk)
        context = {'partner': detail, 'Products': product}

        return render(request, 'Policy/partnerDetail.html', context)


class BusinessPartnerCreateView(View):
    def get(self, request):
        product = Product.objects.all()
        agentForm = AgentForm()
        insuranceForm = InsuranceForm()

        context = {
            'Products': product,
            'insuranceForm': insuranceForm,
            'agentForm': agentForm
        }

        return render(request, 'Policy/partnerCreation.html', context)

    def post(self, request, *args, **kwargs):
        product = Product.objects.all()
        context = {'Products': product}

        if 'insurance' in request.POST:
            agentForm = AgentForm()
            insuranceForm = InsuranceForm(request.POST)

            if insuranceForm.is_valid():
                insuranceForm.save()
                return HttpResponseRedirect(reverse('policy:bp_list'))
            else:
                context['insuranceForm'] = insuranceForm
                context['agentForm'] = agentForm

        elif 'agent' in request.POST:
            insuranceForm = InsuranceForm()
            agentForm = AgentForm(request.POST)

            if agentForm.is_valid():
                agentForm.save()
                return HttpResponseRedirect(reverse('policy:bp_list'))
            else:
                context['agentForm'] = agentForm
                context['insuranceForm'] = insuranceForm

        return render(request, 'Policy/partnerCreation.html', context)


class PolicyListView(View):

    def get(self, request):
        product = Product.objects.all()
        policyList = Policy.objects.all().order_by('-id')
        context = {'Policies': policyList, 'Products': product}

        return render(request, 'Policy/policyList.html', context)


class PolicyDetailView(View):

    def get(self, request, pk):
        product = Product.objects.all()
        policyDetail = Policy.objects.get(id=pk)
        if policyDetail.period_of_cover:
            end_date = policyDetail.effective_date + policyDetail.period_of_cover
            context = {'Policy': policyDetail,
                       'End_Date': end_date, 'Products': product}
        else:
            context = {'Policy': policyDetail, 'Products': product}

        return render(request, 'Policy/policyDetail.html', context)


class PolicyCreateView(CreateView):
    model = Policy
    template_name = 'Policy/policyCreation.html'
    form_class = HolderForm
    success_url = '/policy/list'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PolicyCreateView, self).get_context_data(**kwargs)
        # for navbar product list
        context['Products'] = Product.objects.all()
        # get URL params
        context['productName'] = self.kwargs['product'].replace('-', ' ')

        product_id = Product.objects.get(
            product=self.kwargs['product'].replace('-', ' '))
        if self.request.POST:
            context['policy'] = PolicyFormSet(self.request.POST,  form_kwargs={
                'product_id': product_id.id})
        else:
            context['policy'] = PolicyFormSet(
                form_kwargs={'product_id': product_id.id})

        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """

        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        context = self.get_context_data()
        policy_form = context['policy']
        if (form.is_valid() and policy_form.is_valid()):
            return self.form_valid(form, policy_form)
        else:

            return self.form_invalid(form, policy_form)

    def form_valid(self, form, policy_form):
        """
        Called if all forms are valid. Creates a Holder instance along with
        associated policy and then redirects to a
        success page.
        """
        self.object = form.save()
        policy_form.instance = self.object
        policy_form.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, policy_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  policy=policy_form))

    # def get_form_kwargs(self):
    #     kwargs = super(PolicyCreateView, self).get_form_kwargs()
    #     # update the kwargs for the form init method with yours
    #     # kwargs.update(self.kwargs)  # self.kwargs contains all url conf params
    #     product_id = Product.objects.values(
    #         'id').get(product=self.kwargs['product'])
    #     kwargs["product_id"] = product_id.id
    #     return kwargs
