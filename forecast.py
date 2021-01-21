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
        print(api_key)
        r = requests.get('http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'.format(city=city, api_key=api_key))
        lista = r.json()['list']

        #for date, value in groupby(lista, key = lambda x : datetime.utcfromtimestamp(x['dt']).date() ):
        groups = []
        for date, value in sort_and_group(lista, key = lambda x : datetime.utcfromtimestamp(x['dt']).date() ):
            groups.append(list(value))
            lo,hi = sys.maxsize,-sys.maxsize-1
            for item in groups:
                for x in item:
                    lo = min(x['main']['temp_min'], lo)
                    hi = max(x['main']['temp_max'], hi)
 

            #print(type(value))
            #minmin = min(value, key=lambda x: x['main']['temp_min'])
            #list_temp_min = sort_and_group(value, key=lambda x: x['main']['temp_min']) 
            #print('*****')
            #print(type(minmin))
            ##temp_min = (min(x) for _, x in list_temp_min)
            #sorted_by_temp = sorted(temp_min, key=lambda x: x['main']['temp_min'])
            #minmin = min(islice(grouper(sorted_by_temp, 1), 1))
            self.list.append( {'date' : date.strftime('%d/%m/%Y'), 'temp_min' : lo, 'temp_max' : hi} )




    def __lt__(self, other):
        return self.time < other.time


def sort_and_group(iterable, key=None):
    return groupby(sorted(iterable, key=key), key=key)

def grouper(iterable, n, fillvalue=None):
    iters = [iter(iterable)] * n
    return zip_longest(*iters, fillvalue=fillvalue)


