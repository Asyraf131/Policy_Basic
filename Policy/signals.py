from django.dispatch import receiver
from django.core.signals import request_finished, request_started
from .models import PolicyStatus, PolicyTransactionType, PartnerRole, PartnerType, Product, Policy, BusinessPartner
from django.dispatch import Signal


@receiver(request_started)
def log_request(sender, environ, **kwargs):
    method = environ['REQUEST_METHOD']
    host = environ['HTTP_HOST']
    path = environ['PATH_INFO']
    query = environ['QUERY_STRING']
    query = '?' + query if query else ''
    print(' ----  New Request -> {method} {host}{path}{query} ----'.format(
        method=method,
        host=host,
        path=path,
        query=query,
    ))


new_policy = Signal(
    providing_args=["policy", "holder", "insurance", "agent", "product"])
