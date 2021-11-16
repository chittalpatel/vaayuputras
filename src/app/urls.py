from django.urls import path

from . import views

urlpatterns = [
    # path for home page
    path('', views.index, name='home'),
    # path for dashboard
    path('dashb',views.dashb, name='dashb'),
    # path for dashboard non authenticated
    path('dashbnonauth',views.dashb, name='dashbnonauth'),
    # path for wind farm which is available in database
    path('wffromdb',views.wffromdb, name='wffromdb'),
    path('wfmanual',views.wfmanual, name='wfmanual'),
    path('setupwindfarm',views.setupwindfarm, name='setupwindfarm'),
    path('map',views.map, name='map'),
    path('contactus',views.contactus, name='contactus'),
    path('userHome',views.userHome, name='userHome'),
    path('gettraindata',views.gettraindata, name='gettraindata'),
    path('deletemodel',views.deletemodel, name='deletemodel'),
    path('health', views.health, name='health'),
    path('404', views.handler404, name='404'),
    path('500', views.handler500, name='500'),
]
