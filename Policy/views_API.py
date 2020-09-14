from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import PolicyStatus, PolicyTransactionType, PartnerRole, PartnerType, Product, Policy, BusinessPartner
from .serializers import PolicySerializer, BusinessPartnerSerializer, NewPolicySerializer


class APIOverview(APIView):
    def get(self, request):
        api_urls = {
            'api/',
            'api/policy/list',
            'api/policy/detail/<int:pk>',
            'api/partner/list',
            'api/partner/detail/<int:pk>'
        }
        return Response(api_urls)


class PolicyListView(APIView):
    def get(self, request):
        policyList = Policy.objects.all().order_by('-id')
        serializer = PolicySerializer(policyList, many=True)
        return Response(serializer.data)


class PolicyCreateView(APIView):
    def post(self, request):
        serializer = NewPolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PolicyDetailView(APIView):

    def get_object(self, pk):
        try:
            return Policy.objects.get(id=pk)
        except Policy.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        policy = self.get_object(pk)
        serializer = PolicySerializer(policy)
        return Response(serializer.data)

    def put(self, request, pk):
        policy = self.get_object(pk)
        serializer = PolicySerializer(policy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        policy = self.get_object(pk)
        policy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PartnerListView(APIView):
    def get(self, request):
        PartnerList = BusinessPartner.objects.all().order_by('-id')
        serializer = BusinessPartnerSerializer(PartnerList, many=True)
        return Response(serializer.data)


class PartnerCreateView(APIView):
    def post(self, request):
        serializer = BusinessPartnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartnerDetailView(APIView):

    def get_object(self, pk):
        try:
            return BusinessPartner.objects.get(id=pk)
        except BusinessPartner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        partner = self.get_object(pk)
        serializer = BusinessPartnerSerializer(partner)
        return Response(serializer.data)

    def put(self, request, pk):
        partner = self.get_object(pk)
        serializer = BusinessPartnerSerializer(partner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        partner = self.get_object(pk)
        partner.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
