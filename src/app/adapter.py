from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import custom_field

class MyAccountAdapter(DefaultAccountAdapter):

    # Login is redirected here
    def get_login_redirect_url(self, request):
        # Check for user has been provided custom field or not
        if custom_field.objects.get(user__username__exact=request.user.username).capacity is None:
            # if not redirect to map
            return "/map"
        else:
            # if has been provided redirect to userHome page
            return "/userHome"