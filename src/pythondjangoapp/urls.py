from django.contrib import admin

from django.urls import path
from django.conf.urls import include

urlpatterns = [
                path('', include('app.urls')),
                path('admin/', admin.site.urls),
                path('accounts/',include('allauth.urls')),
                path('api/',include('api.urls')),
               ]