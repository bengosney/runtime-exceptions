from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

import requests
from math import sin, cos, sqrt, atan2, radians
from functools import lru_cache
        
from datetime import datetime
import time
from django.utils import timezone
from django.utils.timezone import make_aware

from websettings.models import setting

from pprint import pprint
    
class Runner(models.Model):
    stravaID = models.CharField(max_length=200, unique=True)
    access_token = models.CharField(max_length=512)
    #access_expires = models.DateTimeField(default=datetime.now)
    access_expires = models.CharField(max_length=512)    
    refresh_token = models.CharField(max_length=512)    

    @staticmethod
    def getAuthUrl(request):
        url = "https://www.strava.com/api/v3/oauth/authorize"

        redirect_uri = request.build_absolute_uri(reverse('auth_callback'))
        params = { 'client_id': setting.getValue('client_id'),
                   'redirect_uri': redirect_uri, 'response_type': 'code',
                   'approval_prompt': 'auto', 'scope':
                   'activity:write,activity:read_all,read,profile:write,read_all', }
        
        p = requests.Request('GET', url, params=params).prepare()

        return p.url


    @classmethod
    def authCallBack(cls, code):
        url = "https://www.strava.com/api/v3/oauth/token"
        data = {
            'client_id': setting.getValue('client_id'),
            'client_secret': setting.getValue('client_secret'),
            'code': code,
            'grant_type': 'authorization_code',
        }

        headers = {
            'Accept': "application/json",            
            'Cache-Control': "no-cache",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
        }

        response = requests.request("POST", url, headers=headers, data=data)

        data = response.json()

        if response.status_code != 200:
            return False

        expires = data['expires_at'] #make_aware(datetime.fromtimestamp(data['expires_at']))     

        runner, _ = cls.objects.get_or_create(
            stravaID=data['athlete']['id'],
            access_token=data['access_token'],
            access_expires=expires,
            refresh_token=data['refresh_token'],
        )

        runner.save()
        return True


    def refreshToken(self):
        print("Refreshing token")
        url = 'https://www.strava.com/api/v3/oauth/token'
        data = {
            'client_id': setting.getValue('client_id'),
            'client_secret': setting.getValue('client_secret'),
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token',
        }

        headers = {
            'Accept': "application/json",            
            'Cache-Control': "no-cache",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
        }

        response = requests.request("POST", url, headers=headers, data=data)

        data = response.json()

        if response.status_code != 200:
            return False
        
        self.access_token = data['access_token']
        self.access_expires = data['expires_at'] #str(datetime.fromtimestamp(data['expires_at']))
        self.refresh_token = data['refresh_token']
        self.save()

    @property
    def authCode(self):
        if int(self.access_expires) < time.time(): #timezone.now():
            self.refreshToken()

        return self.access_token


    @classmethod
    def getAuthenticatedAthlete(cls):
        pass

    @lru_cache(512)
    def makeCall(self, path, args={}):
        url = f'https://www.strava.com/api/v3/{path}'

        headers = {
            'Accept': "application/json",            
            'Cache-Control': "no-cache",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'Authorization': f"Bearer {self.authCode}"
        }
        
        data = requests.get(url, headers=headers)

        if data.status_code == 200:
            return data.json()

        return False

    def getDetails(self):
        return self.makeCall('athlete')
    
    def getActivities(self):
        return self.makeCall('athlete/activities')

    def activity(self, activityID):
        return self.makeCall(f'activities/{activityID}')

    def distanceFrom(self):
        pass

    @staticmethod
    def getDistance(point1, point2):
        R = 6373.0

        lat1 = radians(point1[0])
        lon1 = radians(point1[1])
        lat2 = radians(point2[0])
        lon2 = radians(point2[1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c

        return distnce
    

class Renamer(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    name = models.CharField(max_length=200)
    number = models.IntegerField()
