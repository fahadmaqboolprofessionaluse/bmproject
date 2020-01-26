from django.contrib import admin
from django.urls import re_path
from django.conf.urls import url, include
from .views import person_api,get_data_api,make_csv,get_file
from rest_auth.registration.views import VerifyEmailView, RegisterView


urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
       re_path(r'^account-confirm-email/', VerifyEmailView.as_view(),
     name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
     name='account_confirm_email'),
    url('process-evaluation',get_data_api),
    url('generate_csv', make_csv),
    url('show-files', get_file),
    
    
]