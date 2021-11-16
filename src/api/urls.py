from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # Path for API Docs
    path('', views.apiHome, name='apiHome'),
    # Path for showing selected wind farm list from database
    path('windfarm_list', views.windfarm_list, name='windfarm_list'),
    # API for general prediction
    path('prediction/<str:name>', views.prediction_list.as_view(), name='prediction_list'),
    # API for specific hours general prediction
    path('prediction/<str:name>/<int:hour>', views.prediction_detail.as_view(), name='prediction'),
    # API for user's wind farm prediction
    path('user_prediction', views.user_prediction_list.as_view(), name='user_prediction_list'),
    # API for specific hours user's wind farm prediction
    path('user_prediction/<int:hour>', views.user_prediction_detail.as_view(), name='user_prediction_detail'),
    # API for economics calculator
    path('eco_calc/<str:FCR>/<str:IC>/<str:WFC>/<str:CF>/<str:RPKWh>/<str:LLC>', views.eco_calc.as_view(),
         name='eco_calc'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
