from dataimport import weatherData, DataReader

__author__ = 'Daniel Puschmann'
import os
import json
fields = None
# cities = ['Hinnerup', 'Horning', 'Skanderborg']
cities = ['Skanderborg']
for city in cities:
    print 'splitting for %s' % city
    data_path = 'data//WeatherData AugustSeptember//%s//' % city
    stream_path = 'data//WeatherData AugustSeptember//%s//streams\\' % city
    for file_name in os.listdir(data_path):
        if file_name.endswith('.txt'):
            f = data_path+'\\'+file_name
            reader = DataReader()

            weather_data = weatherData.WeatherData(f)
            if fields is None:
                fields = weather_data.hourly_observations[0].keys()

            for field in fields:
                if field == 'timestamp':
                    continue
                stream_file_name = stream_path + str(field) +'.txt'
                field_data = weather_data.field2dict(field)

                with open(stream_file_name, 'a') as stream_file:
                    json.dump(field_data, stream_file)
                    stream_file.write('\n')


