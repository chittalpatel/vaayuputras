from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import wind_farm
from app.views import get_prediction, eco_calc_


# Render API Docs Page
def apiHome(request):
    wind_farm_list = wind_farm.objects.all().order_by('name')
    return render(request, 'api/apiDocs.html', {'wind_farm_data': wind_farm_list})


# Render selected wind farm from database
def windfarm_list(request):
    # Get all wind farm object from database
    wind_farm_list = wind_farm.objects.all().order_by('name')
    return render(request, 'api/windfarm_list.html', {'wind_farm_data': wind_farm_list})


# API view for general prediction
class prediction_list(APIView):
    # AllowAny user to use this API
    permission_classes = [AllowAny]

    # Input is only wind farm name
    def get(self, request, name, format=None):

        data = dict({})
        # Check for weather wind farm name is exist or not
        try:
            # If exist get wind farm object
            wind_farm_details = wind_farm.objects.get(name=name)
        except wind_farm.DoesNotExist:
            # If not exist return error message
            data['detail'] = 'Wind Farm is not in list'
            return Response(data)

        # get_prediction return 72hrs power prediction list for that wind farm
        power_list = get_prediction(wind_farm_details.latitude, wind_farm_details.longitude, wind_farm_details.capacity)
        data_list = []
        # Convert prediction list into JSON dict format
        for i in range(48):
            data_list.append({'hour': (i + 1), 'wind_power': power_list[i]})
        # No Of Turbines is an optional field, So first check for that is available or not. If not then do not return
        if wind_farm_details.noofturbines is None:
            # Arrange data in API Response
            data = {'capacity': wind_farm_details.capacity,
                    'country': wind_farm_details.country,
                    'data': data_list,
                    'latitude': wind_farm_details.latitude,
                    'longitude': wind_farm_details.longitude,
                    'name': name,
                    'place': wind_farm_details.place
                    }
        else:
            # Arrange data in API Response
            data = {'capacity': wind_farm_details.capacity,
                    'country': wind_farm_details.country,
                    'data': data_list,
                    'latitude': wind_farm_details.latitude,
                    'longitude': wind_farm_details.longitude,
                    'name': name,
                    'noofturbines': wind_farm_details.noofturbines,
                    'place': wind_farm_details.place
                    }
        # Return JSON Response
        return Response(data)


# API view for specific hour general prediction
class prediction_detail(APIView):
    # AllowAny user to use this API
    permission_classes = [AllowAny]

    # Input is wind farm name and hour
    def get(self, request, name, hour, format=None):
        data = dict({})
        # Check for weather wind farm name is exist or not
        try:
            # If exist get wind farm object
            wind_farm_details = wind_farm.objects.get(name=name)
        except wind_farm.DoesNotExist:
            # If not exist return error message
            data['detail'] = 'Wind Farm is not in list'
            return Response(data)
        # Check for hour is between 1 and 72
        if type(hour) is not int or hour <= 0 or hour > 48:
            # If not Response with error message
            data['detail'] = 'Invalid Hour'
            return Response(data)
        # get_prediction return 72hrs power prediction list for that wind farm
        power_list = get_prediction(wind_farm_details.latitude, wind_farm_details.longitude, wind_farm_details.capacity)
        # No Of Turbines is an optional field, So first check for that is available or not. If not then do not return
        if wind_farm_details.noofturbines is None:
            # Arrange data in API Response
            data = {'capacity': wind_farm_details.capacity,
                    'country': wind_farm_details.country,
                    'data': [{'hour': hour, 'wind_power': power_list[hour - 1]}],
                    'latitude': wind_farm_details.latitude,
                    'longitude': wind_farm_details.longitude,
                    'name': name,
                    'place': wind_farm_details.place
                    }
        else:
            # Arrange data in API Response
            data = {'capacity': wind_farm_details.capacity,
                    'country': wind_farm_details.country,
                    'data': [{'hour': hour, 'wind_power': power_list[hour - 1]}],
                    'latitude': wind_farm_details.latitude,
                    'longitude': wind_farm_details.longitude,
                    'name': name,
                    'noofturbines': wind_farm_details.noofturbines,
                    'place': wind_farm_details.place
                    }
        return Response(data)


# API view for user's wind farm prediction
class user_prediction_list(APIView):

    # This API is available for authenticated user
    # And for authentication TokenAuthentication is used
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Only API key input is required which is provided in headers of URL
    def get(self, request, format=None):
        # get_prediction return 48hrs power prediction list for that wind farm
        power_list = get_prediction(request.user.custom_field.latitude, request.user.custom_field.longitude,
                                    request.user.custom_field.capacity)
        data_list = []
        # Convert prediction list into JSON dict format
        for i in range(48):
            data_list.append({'hour': (i + 1), 'wind_power': power_list[i]})
        # No Of Turbines is an optional field, So first check for that is available or not. If not then do not return
        if request.user.custom_field.no_turbines is None:
            # Arrange data in API Response
            data = {'capacity': request.user.custom_field.capacity,
                    'country': request.user.custom_field.country,
                    'data': data_list,
                    'farm_name': request.user.custom_field.farm_name,
                    'latitude': request.user.custom_field.latitude,
                    'longitude': request.user.custom_field.longitude,
                    'place': request.user.custom_field.place,
                    'username': request.user.username}
        else:
            # Arrange data in API Response
            data = {'capacity': request.user.custom_field.capacity,
                    'country': request.user.custom_field.country,
                    'data': data_list,
                    'farm_name': request.user.custom_field.farm_name,
                    'latitude': request.user.custom_field.latitude,
                    'longitude': request.user.custom_field.longitude,
                    'no_turbines': request.user.custom_field.no_turbines,
                    'place': request.user.custom_field.place,
                    'username': request.user.username}
        return Response(data)


class user_prediction_detail(APIView):
    # This API is available for authenticated user
    # And for authentication TokenAuthentication is used
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # API key and hour input is required,API key is provided in headers of URL
    def get(self, request, hour, format=None):
        data = dict({})
        # Check for hour is between 1 and 72
        if type(hour) is not int or hour <= 0 or hour > 48:
            # If not Response with error message
            data['detail'] = 'Invalid Hour'
            return Response(data)
        # get_prediction return 72hrs power prediction list for that wind farm
        power_list = get_prediction(request.user.custom_field.latitude, request.user.custom_field.longitude,
                                    request.user.custom_field.capacity)

        # No Of Turbines is an optional field, So first check for that is available or not. If not then do not return
        if request.user.custom_field.no_turbines is None:
            # Arrange data in API Response
            data = {'capacity': request.user.custom_field.capacity,
                    'country': request.user.custom_field.country,
                    'data': [{'hour': hour, 'wind_power': power_list[hour - 1]}],
                    'farm_name': request.user.custom_field.farm_name,
                    'latitude': request.user.custom_field.latitude,
                    'longitude': request.user.custom_field.longitude,
                    'place': request.user.custom_field.place,
                    'username': request.user.username
                    }
        else:
            # Arrange data in API Response
            data = {'capacity': request.user.custom_field.capacity,
                    'country': request.user.custom_field.country,
                    'data': [{'hour': hour, 'wind_power': power_list[hour - 1]}],
                    'farm_name': request.user.custom_field.farm_name,
                    'latitude': request.user.custom_field.latitude,
                    'longitude': request.user.custom_field.longitude,
                    'no_turbines': request.user.custom_field.no_turbines,
                    'place': request.user.custom_field.place,
                    'username': request.user.username
                    }

        return Response(data)


class eco_calc(APIView):
    # AllowAny user to use this API
    permission_classes = [AllowAny]

    # Six input is required, See full documentation in API Documentation
    def get(self, request, FCR, IC, WFC, CF, RPKWh, LLC, format=None):
        data = dict({})

        # Check for all six value is float or int
        try:
            FCR = float(FCR)
            IC = float(IC)
            WFC = float(WFC)
            CF = float(CF)
            RPKWh = float(RPKWh)
            LLC = float(LLC)
        except ValueError:
            # If not response with error message
            data['detail'] = 'Invalid Value'
            return Response(data)

        # check all parameter has a valid value
        # If not response with appropriate error message
        if not 0.5 <= FCR <= 80:
            data['detail'] = 'Invalid Fixed Charge Rate'
            return Response(data)
        elif not 0.1 <= IC <= 10000.00:
            data['detail'] = 'Invalid Investment Capital'
            return Response(data)
        elif not 0.1 <= WFC <= 22000.00:
            data['detail'] = 'Invalid Wind Farm Capacity'
            return Response(data)
        elif not 5 <= CF <= 80:
            data['detail'] = 'Invalid Capacity Factor'
            return Response(data)
        elif not 0 <= RPKWh <= 10:
            data['detail'] = 'Invalid Revenue per kWh'
            return Response(data)
        elif not 0 <= LLC <= 5000000000.00:
            data['detail'] = 'Invalid Land Lease Cost'
            return Response(data)

        # eco_calc return calculated value in dict format
        # See api documentation for input and output value
        output = eco_calc_(FCR, IC, WFC, CF, RPKWh, LLC)

        # Arrange data in API Response
        data = {'FCR': FCR, 'IC': IC, 'WFC': WFC, 'CF': CF, 'RPKWh': RPKWh, 'LLC': LLC,
                'AEP': round(output['AEP'], 2), 'LRC': round(output['LRC'], 2), 'OAM': round(output['OAM'], 2),
                'CTGP': round(output['CTGP'], 2), 'Tae': round(output['Tae'], 2),
                'GI': round(output['GI'], 2), 'AP': round(output['AP'], 2), 'ROI': round(output['ROI'], 2),
                'BEP': round(output['BEP'], 2)}
        return Response(data)
