from django.urls import include, path
from . import views
from . import views_API

app_name = 'policy'

urlpatterns = [
    path('',
         views.NavBar.as_view(), name='navBar'),
    path('partner/list/',
         views.BusinessPartnerListView.as_view(), name='bp_list'),
    path('partner/detail/<int:pk>/<str:type>/',
         views.BusinessPartnerDetailView.as_view(), name='bp_detail'),
    path('partner/create/',
         views.BusinessPartnerCreateView.as_view(), name='partner_create'),
    path('policy/list/',
         views.PolicyListView.as_view(), name='policy_list'),
    path('policy/detail/<int:pk>/',
         views.PolicyDetailView.as_view(), name='policy_detail'),
    path('policy/<str:product>/create/',
         views.PolicyCreateView.as_view(), name='policy_create'),

    ################################# API View #################################

    path('api/', views_API.APIOverview.as_view(), name='api_overview'),
    path('api/policy/list/', views_API.PolicyListView.as_view(), name='policy-list'),
    path('api/policy/create/', views_API.PolicyCreateView.as_view(),
         name='policy-create/'),
    path('api/policy/detail/<int:pk>/',
         views_API.PolicyDetailView.as_view(), name='policy-detail'),
    path('api/partner/list/', views_API.PartnerListView.as_view(), name='partner-list'),
    path('api/partner/create/', views_API.PartnerCreateView.as_view(),
         name='partner-create/'),
    path('api/partner/detail/<int:pk>/',
         views_API.PartnerDetailView.as_view(), name='partner-detail'),
]
