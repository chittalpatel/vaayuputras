
# Commented Part

# from django.db import models
# from app.models import wind_farm,custom_field
# from django.contrib.auth.models import User
# class power_prediction(models.Model):
#     hour = models.IntegerField()
#     wind_power=models.FloatField(null=True)
#     farm=models.ForeignKey(wind_farm,on_delete=models.CASCADE,related_name='data')
#     class Meta:
#         unique_together = ['farm', 'hour']
#         ordering = ['hour']
#
# class user_power_prediction(models.Model):
#     hour = models.IntegerField()
#     wind_power = models.FloatField(null=True)
#     user = models.ForeignKey(custom_field, on_delete=models.CASCADE, related_name='data')
#
#     class Meta:
#         unique_together = ['user', 'hour']
#         ordering = ['hour']
#
# class economic_calculator(models.Model):
#     FCR = models.FloatField(primary_key=True)
#     IC = models.FloatField(null=True)
#     WFC = models.FloatField(null=True)
#     CF = models.FloatField(null=True)
#     RPKWh = models.FloatField(null=True)
#     LLC = models.FloatField(null=True)
#     AEP = models.BigIntegerField(null=True)
#     LRC = models.BigIntegerField(null=True)
#     OAM = models.BigIntegerField(null=True)
#     CTGP = models.FloatField(null=True)
#     Tae = models.BigIntegerField(null=True)
#     GI = models.BigIntegerField(null=True)
#     AP = models.BigIntegerField(null=True)
#     ROI = models.FloatField(null=True)
#     BEP = models.IntegerField(null=True)
#
#
#
#
#
