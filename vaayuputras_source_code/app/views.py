#importing all necessary libraries
from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
from django.http import Http404
from django.shortcuts import render, redirect, HttpResponse
from rest_framework.authtoken.models import Token
import json
import requests
import numpy as np
from watson_machine_learning_client import WatsonMachineLearningAPIClient
from keras.models import load_model
from app.models import user_models
from app.dltrain import TrainModel
from app.forms import UploadFileForm
import logging
from django.conf import settings
import os

#logger to log details, useful for testing purpose
logger=logging.getLogger('app_api')

#method to render home page
def index(request):
    return render(request, 'home.html')

#method to render selecting wind farm dashboard page
def dashb(request):
    if request.user.is_authenticated:
        return render(request, 'dashb.html')
    else:
        return render(request, 'dashbnonauth.html')

#render setupwindfarm page
def setupwindfarm(request):
    return render(request, 'setupwindfarm.html')

#render contactus page
def contactus(request):
    return render(request, 'contactus.html')

#deal with request where user selected wind farm from database
def wffromdb(request):
    if request.method=='POST':
        string=json.loads(request.POST['wind_farms'])
        #get wind farm details
        windfarmDetails={'Name':string['Name'],
                         'Place':string['Place'],
                         'Country':string['Country'],
                         'Capacity':string['Capacity']
                         }
        #get latitude and longitude of wind farm
        coordinates={'Latitude':string['Latitude'],
                     'Longitude':string['Longitude']
                     }
    elif request.method=='GET':
        if request.user.is_authenticated:
            # this if will be true when user clicks Go To Dashboard button from Userhome
            #All the details of user's own wind farm will be stored in the table custom_field
            windfarmDetails = {'Name': request.user.custom_field.farm_name,
                           'Place': request.user.custom_field.place,
                           'Country': request.user.custom_field.country,
                           'Capacity': request.user.custom_field.capacity
                           }
            coordinates = {'Latitude': request.user.custom_field.latitude,
                       'Longitude': request.user.custom_field.longitude
                           }
        else:
            return render(request,'home.html')
    else:
        return render(request,'home.html')

    #make a call to open weather map api and clima cell api to get 72 hours wind speed and wind direction prediction
    res = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?lat={coordinates["Latitude"]}&lon={coordinates["Longitude"]}&appid=8dca2ad4788f6d0b4166dc8a91f404cb')
    output = res.json()
    windspeed = []
    wr = np.zeros((6, 8))
    #extract wind speed and wind direction from response
    for weather in output['hourly']:
        wd = weather['wind_deg']
        ws_ = weather['wind_speed']
        windspeed.append(ws_)
        #below code is to process the data for input to wind rose chart to frontend
        idx = getDirIdx(wd)
        if 0 <= ws_ <= 5:
            wr[0][idx] += 1
        elif 5 < ws_ <= 10:
            wr[1][idx] += 1
        elif 10 < ws_ <= 15:
            wr[2][idx] += 1
        elif 15 < ws_ <= 20:
            wr[3][idx] += 1
        elif 20 < ws_ <= 25:
            wr[4][idx] += 1
        elif ws_ > 25:
            wr[5][idx] += 1

    res = requests.get(
        f'https://api.climacell.co/v3/weather/forecast/hourly?lat={coordinates["Latitude"]}&lon={coordinates["Longitude"]}&start_time=now&fields[]=wind_speed&fields[]=wind_direction&apikey=596Un0cOu5hRrSNTrKCXykM5Q3N7NOSX')
    output = res.json()
    for weather in output[48:72]:
        wd = weather['wind_direction']['value']
        ws_ = weather['wind_speed']['value']
        windspeed.append(weather['wind_speed']['value'])
        idx = getDirIdx(wd)
        if 0 <= ws_ <= 5:
            wr[0][idx] += 1
        elif 5 < ws_ <= 10:
            wr[1][idx] += 1
        elif 10 < ws_ <= 15:
            wr[2][idx] += 1
        elif 15 < ws_ <= 20:
            wr[3][idx] += 1
        elif 20 < ws_ <= 25:
            wr[4][idx] += 1
        elif ws_ > 25:
            wr[5][idx] += 1

    #multiplying by 100 and dividing by 72 to get frequency distribution
    wr = wr * 100 / 72
    # convert to a form in which we can give input to deployed model
    inputwindspeed=[[[ws / 25]] for ws in windspeed]

    try:
        #check if user wants to get predictions from custom model
        custom_model=request.GET['custom_model']
        logger.info(custom_model)
    except:
        custom_model='no'

    if custom_model=='yes':
        logger.info('Inside Custom Model')
        #get name of custom model as name of user personal model is his api key
        api=Token.objects.get(user_id=request.user.custom_field.user_id).key
        #create an object to load model
        model=TrainModel(api,inputwindspeed,None,float(windfarmDetails['Capacity']),True)
        #predict the wind power using user personal model.
        windpower=model.predict()
        del model

    else:
        #use our general model for inference purpose which is deployed
        wml_credentials = {
            "apikey": "BDA_0HBFsVaW71HJCcx9e16th3uVf_QdHx1oOYjgMglu",
            "iam_apikey_description": "Auto-generated for key 09502a19-c0c6-404e-8bb7-a2c2b96e8b50",
            "iam_apikey_name": "wdp-writer",
            "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
            "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/12b13c28e9fc4fe2ab90672aebc2e634::serviceid:ServiceId-30133df9-5233-40b7-838c-3596b739ca64",
            "instance_id": "03f6c780-754c-45aa-b8b6-b3f83d25549f",
            "url": "https://eu-gb.ml.cloud.ibm.com"
    }
        #create client for getting predictions
        client = WatsonMachineLearningAPIClient(wml_credentials)
        scoring_endpoint = '1ff9e07f-b578-4967-b39c-4744c8f0c5cd'
        #call WML API to get predictions
        response_scoring = client.deployments.score(scoring_endpoint, {client.deployments.ScoringMetaNames.INPUT_DATA:
                                                                           [{'values': inputwindspeed
                                                                             }]
                                                                       })

        logger.info(response_scoring)
        #clean the response to give to the frontend
        windpower = []
        for preds in response_scoring['values']:
            windpower.append(preds[0][0][0]*float(windfarmDetails['Capacity']))


    #pass static maps url to disply static maps on dashboard
    staticmaps=f"https://maps.googleapis.com/maps/api/staticmap?center={coordinates['Latitude']},{coordinates['Longitude']}&zoom=9&size=600x300&maptype=roadmap&markers=color:red%7C{coordinates['Latitude']},{coordinates['Longitude']}&key=YOUR_KEY_HERE"

    if request.user.is_authenticated:
        #render dashboard with data
        return render(request, 'dashbload.html',{'powerdata':windpower,
                                                 'windspeeddata':windspeed,
                                                 'windrose':[list(wr_) for wr_ in wr],
                                                 'windfarmDetails':windfarmDetails,
                                                 'coordinates':coordinates,
                                                 'staticmaps':staticmaps
                                                 })
    else:
        return render(request, 'dashbloadnonauth.html', {'powerdata': windpower,
                                                      'windspeeddata': windspeed,
                                                      'windrose': [list(wr_) for wr_ in wr],
                                                      'windfarmDetails': windfarmDetails,
                                                      'coordinates': coordinates,
                                                      'staticmaps':staticmaps
                                                      })


#method to serve requests when user select wind farms manually from google maps
def wfmanual(request):
    if request.method=='POST':
        #process response
        details=request.POST['wfdetails'].split(',')
        coords=request.POST['wfcoords'][:-1].split(', ')
        capacity=request.POST['wfcapacity']
        #make dictionary of wind farm details and coordinates
        windfarmDetails={'Name':details[0],
                         'Place':details[1],
                         'Country':details[2],
                         'Capacity':capacity
                         }
        coordinates = {'Latitude': coords[0],
                       'Longitude': coords[1]
                       }
        # Make calls to open weather map api and clima cell api to get 72 hours weatehr forecast
        res = requests.get(
            f'https://api.openweathermap.org/data/2.5/onecall?lat={coordinates["Latitude"]}&lon={coordinates["Longitude"]}&appid=8dca2ad4788f6d0b4166dc8a91f404cb')
        output = res.json()
        windspeed = []
        wr = np.zeros((6, 8))
        #extract wind speed and wind direction from response
        for weather in output['hourly']:
            wd = weather['wind_deg']
            ws_ = weather['wind_speed']
            windspeed.append(ws_)
            #below code is to process the data to give input to windrose chart in frontend
            idx = getDirIdx(wd)
            if 0 <= ws_ <= 5:
                wr[0][idx] += 1
            elif 5 < ws_ <= 10:
                wr[1][idx] += 1
            elif 10 < ws_ <= 15:
                wr[2][idx] += 1
            elif 15 < ws_ <= 20:
                wr[3][idx] += 1
            elif 20 < ws_ <= 25:
                wr[4][idx] += 1
            elif ws_ > 25:
                wr[5][idx] += 1

        res = requests.get(
            f'https://api.climacell.co/v3/weather/forecast/hourly?lat={coordinates["Latitude"]}&lon={coordinates["Longitude"]}&start_time=now&fields[]=wind_speed&fields[]=wind_direction&apikey=596Un0cOu5hRrSNTrKCXykM5Q3N7NOSX')
        output = res.json()
        for weather in output[48:72]:
            wd = weather['wind_direction']['value']
            ws_ = weather['wind_speed']['value']
            windspeed.append(weather['wind_speed']['value'])
            idx = getDirIdx(wd)
            if 0 <= ws_ <= 5:
                wr[0][idx] += 1
            elif 5 < ws_ <= 10:
                wr[1][idx] += 1
            elif 10 < ws_ <= 15:
                wr[2][idx] += 1
            elif 15 < ws_ <= 20:
                wr[3][idx] += 1
            elif 20 < ws_ <= 25:
                wr[4][idx] += 1
            elif ws_ > 25:
                wr[5][idx] += 1

        # multiplying by 100 and dividing by 72 to get frequency distribution
        wr = wr * 100 / 72
        # convert to a form in which we can give input to deployed model
        inputwindspeed = [[[ws / 25]] for ws in windspeed]

        wml_credentials = {
            "apikey": "BDA_0HBFsVaW71HJCcx9e16th3uVf_QdHx1oOYjgMglu",
            "iam_apikey_description": "Auto-generated for key 09502a19-c0c6-404e-8bb7-a2c2b96e8b50",
            "iam_apikey_name": "wdp-writer",
            "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
            "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/12b13c28e9fc4fe2ab90672aebc2e634::serviceid:ServiceId-30133df9-5233-40b7-838c-3596b739ca64",
            "instance_id": "03f6c780-754c-45aa-b8b6-b3f83d25549f",
            "url": "https://eu-gb.ml.cloud.ibm.com"
        }
        client = WatsonMachineLearningAPIClient(wml_credentials)
        scoring_endpoint = '1ff9e07f-b578-4967-b39c-4744c8f0c5cd'
        response_scoring = client.deployments.score(scoring_endpoint, {client.deployments.ScoringMetaNames.INPUT_DATA:
                                                                           [{'values': inputwindspeed
                                                                             }]
                                                                       })

        windpower = []
        for preds in response_scoring['values']:
            windpower.append(preds[0][0][0] * float(windfarmDetails['Capacity']))

        staticmaps = f"https://maps.googleapis.com/maps/api/staticmap?center={coordinates['Latitude']},{coordinates['Longitude']}&zoom=9&size=600x300&maptype=roadmap&markers=color:red%7C{coordinates['Latitude']},{coordinates['Longitude']}&key=YOUR_KEY_HERE"

        if request.user.is_authenticated:
            return render(request, 'dashbload.html',{'powerdata':windpower,
                                                 'windspeeddata':windspeed,
                                                 'windrose':[list(wr_) for wr_ in wr],
                                                 'windfarmDetails':windfarmDetails,
                                                 'coordinates':coordinates,
                                                 'staticmaps':staticmaps
                                                 })
        else:
            return render(request, 'dashbloadnonauth.html', {'powerdata': windpower,
                                                      'windspeeddata': windspeed,
                                                      'windrose': [list(wr_) for wr_ in wr],
                                                      'windfarmDetails': windfarmDetails,
                                                      'coordinates': coordinates,
                                                      'staticmaps':staticmaps
                                                      })

    else:
        redirect('/')

#request to assign or change user personal wind farm.
def map(request):
        if request.user.is_authenticated:
            if request.method=='POST':
                #token is api key
                if Token.objects.filter(user_id=request.user).exists():
                    #if will be true if user needs to change wind farm
                    token = 0
                else:
                    #else will be true if user is selecting personal wind farm for first time
                    token = Token.objects.create(user=request.user)
                #all the data is collected from post resquest and updated in database
                request.user.custom_field.capacity = float(request.POST['windfarmcapacity'])
                request.user.custom_field.farm_name = request.POST['windfarmname']
                request.user.custom_field.place = request.POST['windfarmplace']
                request.user.custom_field.country = request.POST['windfarmcountry']
                request.user.custom_field.latitude = float(request.POST['windfarmlatitude'])
                request.user.custom_field.longitude = float(request.POST['windfarmlongitude'])
                try:
                    request.user.custom_field.no_turbines = int(request.POST['windfarmnoofturbines'])
                except:
                    request.user.custom_field.no_turbines = None
                request.user.custom_field.save()
                try:
                    #get api key for the user
                    api = Token.objects.get(user_id=request.user.custom_field.user_id).key
                except:
                    #usually this except will never be called by for testing purpose we kept it.
                    api='static_api_key_test'
                if request.user.custom_field.custom_model:
                    #this if will be true if the user has previously trained any personal model for his wind farm
                    um=user_models.objects.get(user_id=request.user.custom_field.user_id)
                    model_name=um.name
                    date_created=um.created_at
                    date_updated=um.updated_at
                    return render(request, "userHome.html", {'api': api,
                                                             'model_name':model_name,
                                                             'date_created':date_created,
                                                             'date_updated':date_updated})
                else:
                    return render(request,'userHome.html',{'api':api})
            if request.method=='GET':
                return render(request,'map.html',{'message':'Select Wind Farm of your Choice. It is mandatory for availing API Credentials. You can explore the Maps and select any Wind Farm of your Choice'})
        else:
            messages.info(request, "To view this page, Login is required")
            return redirect('/accounts/login/')

#method to handle requests to userhome page
def userHome(request):

    if request.method == 'POST':
        #Check for signup
        if 'password1' in request.POST:
            email = ""
            if 'email' in request.POST:
                email = request.POST['email']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            fname = request.POST['fname']
            lname = request.POST['lname']
            #below all the exceptions will be handled
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists.......!!")
                return redirect('/accounts/signup/')
            elif password1 != password2:
                messages.info(request, "Both password must be same.......!!")
                return render(request, 'account/signup.html',
                              {'username': username, 'email': email, 'fname': fname, 'lname': lname})
            elif str(password1) in username:
                messages.info(request, "Password should not be similar to username.......!!")
                return render(request, 'account/signup.html',
                              {'username': username, 'email': email, 'fname': fname, 'lname': lname})
            elif len(str(password1)) < 8:
                messages.info(request, "password length should be 8 or more.....!!")
                return render(request, 'account/signup.html',
                              {'username': username, 'email': email, 'fname': fname, 'lname': lname})
            elif str(password1).isalpha() or str(password1).isdigit():
                messages.info(request, "Password must contain atleast one letter and number.....!!")
                return render(request, 'account/signup.html',
                              {'username': username, 'email': email, 'fname': fname, 'lname': lname})
            else:
                if email == "":
                    #create user
                    User.objects.create_user(username=username, password=password1, first_name=fname, last_name=lname)
                else:
                    User.objects.create_user(username=username, email=email, password=password1, first_name=fname,
                                             last_name=lname)
                #authenticate user
                user = auth.authenticate(username=username, password=password1)
                #log user in
                auth.login(request, user)
                return redirect('/map')


        #else login
        else:
            username = request.POST['username']
            password = request.POST['password']
            if User.objects.filter(username=username).exists():
                user = auth.authenticate(username=username, password=password)
                if user:
                    auth.login(request, user)
                    try:
                        #user will have to select a personal wind farm first to access to userhome page
                        #if user somehow escapes selecting personal wind farm then he would be again redirected to map page as this try will throw an expception
                        temp=request.user.custom_field.farm_name
                        try:
                            #get api key of user
                            api = Token.objects.get(user_id=request.user.custom_field.user_id).key
                        except:
                            #this is for testing purpose and this except will never activate
                            api = 'static_api_key_test'

                        #check if user has previously trained any personal models
                        if request.user.custom_field.custom_model:
                            um = user_models.objects.get(user_id=request.user.custom_field.user_id)
                            model_name = um.name
                            date_created = um.created_at
                            date_updated = um.updated_at
                            return render(request, "userHome.html", {'api': api,
                                                                     'model_name': model_name,
                                                                     'date_created': date_created,
                                                                     'date_updated': date_updated})
                        else:
                            return render(request, 'userHome.html', {'api': api})
                    except:
                        msg = 'It seems You forgot to select one Wind Farm of Your choice during Sign Up. You need to Select a Wind Farm first.'
                        return render(request,'map.html',{'message':msg})
                else:
                    messages.info(request, "Incorrect Password")
                    return render(request, 'account/login.html', {'username': username})
            else:
                messages.info(request, "Username not found")
                return redirect('/accounts/login/')

    else:
        if request.user.is_authenticated:
            if request.user.custom_field.farm_name is None:
                msg='It seems You forgot to select one Wind Farm of Your choice during Sign Up. You need to Select a Wind Farm first.'
                return render(request,'map.html',{'message':msg})
            try:
                api = Token.objects.get(user_id=request.user.custom_field.user_id).key
            except:
                api = 'static_api_key_test'
            if request.user.custom_field.custom_model:
                um = user_models.objects.get(user_id=request.user.custom_field.user_id)
                model_name = um.name
                date_created = um.created_at
                date_updated = um.updated_at
                return render(request, "userHome.html", {'api': api,
                                                         'model_name': model_name,
                                                         'date_created': date_created,
                                                         'date_updated': date_updated})
            else:
                return render(request, 'userHome.html', {'api': api})
        else:
            messages.info(request, "To view this page, Login is required")
            return redirect('/accounts/login/')


#method to get wind power prediction given latitude, longitude and capacity
#used for API and Chatbot purpose
#explanation same as above wffromdb or wfmanual
def get_prediction(lat,long,cap):
    res = requests.get(
        f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={long}&appid=8dca2ad4788f6d0b4166dc8a91f404cb')
    output = res.json()
    windspeed = []
    wr = np.zeros((6, 8))
    for weather in output['hourly']:
        windspeed.append(weather['wind_speed'])


    res = requests.get(
        f'https://api.climacell.co/v3/weather/forecast/hourly?lat={lat}&lon={long}&start_time=now&fields[]=wind_speed&fields[]=wind_direction&apikey=596Un0cOu5hRrSNTrKCXykM5Q3N7NOSX')
    output = res.json()
    for weather in output[48:72]:
        windspeed.append(weather['wind_speed']['value'])


    inputwindspeed = [[[ws / 25]] for ws in windspeed]

    wml_credentials = {
        "apikey": "BDA_0HBFsVaW71HJCcx9e16th3uVf_QdHx1oOYjgMglu",
        "iam_apikey_description": "Auto-generated for key 09502a19-c0c6-404e-8bb7-a2c2b96e8b50",
        "iam_apikey_name": "wdp-writer",
        "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Writer",
        "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/12b13c28e9fc4fe2ab90672aebc2e634::serviceid:ServiceId-30133df9-5233-40b7-838c-3596b739ca64",
        "instance_id": "03f6c780-754c-45aa-b8b6-b3f83d25549f",
        "url": "https://eu-gb.ml.cloud.ibm.com"
    }
    client = WatsonMachineLearningAPIClient(wml_credentials)
    scoring_endpoint = '1ff9e07f-b578-4967-b39c-4744c8f0c5cd'
    response_scoring = client.deployments.score(scoring_endpoint, {client.deployments.ScoringMetaNames.INPUT_DATA:
                                                                       [{'values': inputwindspeed
                                                                         }]
                                                                   })

    windpower = []
    for preds in response_scoring['values']:
        windpower.append(preds[0][0][0] * float(cap))

    return windpower

#method used to get Wind Farm Economics terms calculated
#method used by API and Chatbot
def eco_calc_(fcr,ic,wfc,cf,rpkwh,llc):
    #calculate economics terms related to wind farm
    aep=wfc*24*365*cf
    lrc=ic/22.5
    oam=aep*rpkwh*0.08
    ctgp=(fcr*ic/aep)+((lrc+oam+llc)/aep)
    tae=ctgp*aep
    gi=rpkwh*aep
    ap=(rpkwh-ctgp)*aep
    roi=ap/ic
    bep=ic/ap

    return {'AEP':aep,'LRC':lrc,'OAM':oam,'CTGP':ctgp,'Tae':tae,'GI':gi,'AP':ap,'ROI':roi,'BEP':bep}

#health page to check heath status of website
def health(request):
    state = {"status": "UP"}
    return JsonResponse(state)


def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

#utility method tu get direction index...used for windrose chart
def getDirIdx(wd):
    if 337.5<wd<=22.5:
        return 0
    elif 22.5<wd<=67.5:
        return 1
    elif 67.5<wd<=112.5:
        return 2
    elif 112.5<wd<=157.5:
        return 3
    elif 157.5<wd<=202.5:
        return 4
    elif 202.5<wd<=247.5:
        return 5
    elif 247.5<wd<=292.5:
        return 6
    else:
        return 7


#method for User personal model trainind
def gettraindata(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #get form fields
            capacity = float(request.POST['capacity'])
            file = request.FILES['file']
            wind_speed = []
            wind_power = []
            logger.info('loc1')
            # process data from uploaded csv file
            for chunk in file.chunks():
                for line in chunk.decode("utf-8").split("\n"):
                    line = line.strip().split(",")
                    try:
                        wind_speed.append(float(line[0]))
                        wind_power.append(float(line[1]))
                    except:
                        continue

            try:
                assert len(wind_power)==len(wind_speed)
                logger.info('loc1.5')
                #get api of user for model naming purpose
                api=Token.objects.get(user_id=request.user.custom_field.user_id).key
                #create object to train model
                Model = TrainModel(api, wind_speed, wind_power, capacity,
                                   request.user.custom_field.custom_model)
                logger.info('loc2')
                #train the model
                success = Model.train()

                #if model trains successfully then save the model, update the database
                if success:
                    if request.user.custom_field.custom_model:
                        user_models.objects.get(user_id=request.user.custom_field.user_id).save()
                    else:
                        um = user_models.objects.create(user_id=request.user.custom_field.user_id, name=api)
                        um.save()
                    request.user.custom_field.custom_model = True
                    request.user.custom_field.save()
                    del Model
                    msg = 'Training Successful! Head to Your Account Home to Get Personalized predictions for Your Wind Farm'
                else:
                    msg = 'Training Unsuccessful... Please Read Instructions carefully and Provide proper Input Training Data'

            except:
                msg = 'Training Unsuccessful... Please Read Instructions carefully and Provide proper Input Training Data'
                success=False
            form = UploadFileForm()
            return render(request, 'model_train.html', {'form': form,'msg':msg,'success':success})
    else:
        form = UploadFileForm()
        return render(request, 'model_train.html', {'form': form})


#request to delete model
def deletemodel(request):
    if request.user.is_authenticated:
        try:
            user_models.objects.get(user_id=request.user.custom_field.user_id).delete()
            logger.info('loc1')
            request.user.custom_field.custom_model=False
            request.user.custom_field.save()
            logger.info('loc2')
            return redirect('userHome')
        except:
            return HttpResponse("You don't have any Model Trained")
