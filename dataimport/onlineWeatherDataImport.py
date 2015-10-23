from datetime import datetime, timedelta
from pprint import pprint

__author__ = 'Daniel Puschmann'

import urllib2
import json


datetimeFormat = '%Y%m%d'
sdate = datetime.strptime('20141001', datetimeFormat)
edate = datetime.strptime('20141002', datetimeFormat)

cities = ['pws:KMNCHASK10']
# cities = ['Horning']

baseuri = 'http://api.wunderground.com/api/c27db4fa59da137a/history_%s/q/DK/%s.json'

for city in cities:
    while sdate < edate:
        uri = baseuri % (sdate.strftime(datetimeFormat), city)

        f = urllib2.urlopen(uri)
        json_string = f.read()
        parsed_json = json.loads(json_string)
        pprint(parsed_json)
        break
        file_name = 'data//WeatherData AugustSeptember//test//weatherData%s.txt' % (city, sdate.strftime(datetimeFormat))
        with open(file_name, 'wb') as json_file:
            json_file.write(json.dumps(json_string, sort_keys=True))


        sdate += timedelta(days=1)
        f.close()
    sdate = datetime.strptime('20140801', datetimeFormat)