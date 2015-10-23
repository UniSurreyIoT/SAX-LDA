import datetime

from dataimport import DataReader

__author__ = 'Daniel Puschmann'

class WeatherData(object):

    def __init__(self, file_name):
        self.file_name = file_name
        self.data_reader = DataReader()
        data = self.data_reader.readJson(self.file_name)
        history = data['history']

        self.daily_summery = history['dailysummary'][0]

        self.hourly_observations = history['observations']
        self.day = self.daily_summery['date']['mday']
        self.month = self.daily_summery['date']['mon']
        self.year = self.daily_summery['date']['year']
        self.distributions = {k: None for k in self.hourly_observations[0]}
        self.x_grids = {k: None for k in self.hourly_observations[0]}

        for observation in self.hourly_observations:
            observation['timestamp'] = self.date2timestampstring(observation)
        sorted(self.hourly_observations, key=lambda obs: obs['timestamp'])


    def date2timestampstring(self, observation):
        datetime_Format = '%Y-%m-%dT%H:%M:%S'
        date_string = '%s-%s-%sT%s:%s:00' % (self.year, self.month, self.day,
                                                observation['date']['hour'],
                                                observation['date']['min'])
        timestamp = datetime.datetime.strptime(date_string, datetime_Format)
        return date_string

    #list of fields available:
    # http://www.wunderground.com/weather/api/d/docs?d=data/history&MR=1
    def field2dict(self, field_name):
        if field_name not in self.hourly_observations[0]:
            raise Exception('The field name you provided is not available in the '
                            'weather data. Please make sure to choose one from '
                            'http://www.wunderground.com/weather/api/d/docs?d=data/history&MR=1')

        field_array = {obs['timestamp']: obs[field_name] for obs in self.hourly_observations}
        values = field_array.values()
        # if self.distributions[field_name] is None:
        #     kernel = kde.gaussian_kde(values)
        #     self.x_grids[field_name] = np.linspace(min(values), max(values), len(values))
        #     self.distributions[field_name] = kernel(self.x_grids[field_name])
            # f, ax = plt.subplots(2)
            # pprint(len(x_grid))
            # pprint(len(kernel(x_grid)))
            # ax[0].plot(x_grid,kernel(x_grid))
            # ax[1].plot(list(xrange(len(values))),values)
            # plt.show()
        return field_array

    def computeDistributionForField(self, field_name):
        if field_name not in self.hourly_observations[0]:
            raise Exception('The field name you provided is not available in the '
                            'weather data. Please make sure to choose one from '
                            'http://www.wunderground.com/weather/api/d/docs?d=data/history&MR=1')
        if self.distributions[field_name] is not None:
            return self.distributions[field_name]
        else:
            self.field2dict(field_name)
            return self.distributions[field_name]
