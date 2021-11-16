
# Commented Part

# from .models import power_prediction
# from rest_framework import serializers
# from app.models import wind_farm, custom_field
# from .models import power_prediction, user_power_prediction
# from django.contrib.auth.models import User
#
#
# class power_prediction_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = power_prediction
#         fields = ['hour', 'wind_power']
#
#
# class wind_farm_serializer(serializers.ModelSerializer):
#     data = power_prediction_serializer(many=True, read_only=True)
#
#     class Meta:
#         model = wind_farm
#         fields = ['name', 'capacity', 'place', 'country', 'latitude', 'longitude', 'noofturbines', 'data']
#
#
# class user_power_prediction_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = user_power_prediction
#         fields = ['hour', 'wind_power']
#
#
# class user_serializer(serializers.ModelSerializer):
#     data = user_power_prediction_serializer(many=True, read_only=True)
#     username = serializers.SerializerMethodField('get_username_from_user')
#
#     class Meta:
#         model = custom_field
#         fields = ['username', 'farm_name', 'capacity', 'place', 'country', 'latitude', 'longitude', 'no_turbines',
#                   'data']
#
#     def get_username_from_user(self, obj):
#         return User.objects.get(pk=obj.pk).username
#
#
#
#
#
