# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Model(database table) contain wind farm related data
class wind_farm(models.Model):
    capacity = models.FloatField()
    name = models.CharField(max_length=100, primary_key=True)
    place = models.CharField(max_length=200)
    country = models.CharField(max_length=30)
    latitude = models.FloatField()
    longitude = models.FloatField()
    noofturbines = models.IntegerField()


# model contain custom data(other than basic data) of user
class custom_field(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    capacity = models.FloatField(null=True)
    farm_name = models.CharField(max_length=100, null=True)
    place = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=30, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    no_turbines = models.IntegerField(null=True)
    custom_model = models.BooleanField(null=True)


# model contain trained model(ML model) related data
class user_models(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# When any user account create this  function taking care of, for every user custom field is created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = custom_field.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)
