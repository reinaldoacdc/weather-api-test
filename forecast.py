import requests
import sys
import os
import json
from itertools import groupby, islice, zip_longest
from operator import itemgetter
from datetime import datetime

class Forecast(object):

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)    

    def __init__(self, city):
        self.city = city
        self.list = []

        api_key=os.environ.get('OPENWEATHER_API_KEY')
        r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=pt_br'.format(city=city, api_key=api_key))
        lista = r.json()['list']

        #for date, value in groupby(lista, key = lambda x : datetime.utcfromtimestamp(x['dt']).date() ):
        groups = []
        for date, value in sort_and_group(lista, key = lambda x : datetime.utcfromtimestamp(x['dt']).date() ):
            groups.append(list(value))
            lo,hi = sys.maxsize,-sys.maxsize-1
            for item in groups:
                for x in item:
                    description = x['weather'][0]['description']
                    pressure = x['main']['pressure']
                    humidity = x['main']['humidity']
                    lo = min(x['main']['temp_min'], lo)
                    hi = max(x['main']['temp_max'], hi)
 
            self.list.append( {'date' : date.strftime('%d/%m/%Y'), 'temp_min' : lo, 'temp_max' : hi, 'description' : description, 'pressure' : pressure, 'humidity' : humidity  } )




    def __lt__(self, other):
        return self.time < other.time


def sort_and_group(iterable, key=None):
    return groupby(sorted(iterable, key=key), key=key)

def grouper(iterable, n, fillvalue=None):
    iters = [iter(iterable)] * n
    return zip_longest(*iters, fillvalue=fillvalue)


