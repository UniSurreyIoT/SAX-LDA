__author__ = 'Daniel Puschmann'

from dataPandas import Stream
from datetime import datetime, timedelta
from pprint import pprint
from sax import sax
import os
from genericRule import GenericRule



def read_in_stream(path, file_name):
    stream = Stream(path, file_name)
    features = stream.get_feature_names()
    return stream, features

def extractLabelsToDocument(start, duration, stream, distributions, x_grids, rules, alphabets, prnt=False):
    features = stream.get_feature_names()
    label_end = start + timedelta(hours=duration)
    labels = []
    for feature in features:
        if feature in distributions:
            alphabet = alphabets[feature]
            statistics = {feature: stream.get_statistics(feature, start, label_end) for feature in features}
            data_input = stream.get_time_window(feature, start, label_end)
            pattern = make_word(data_input, alphabet, distributions[feature], x_grids[feature])
            label = rules[feature].apply(pattern, statistics)
            labels.append(str(label))
        if prnt:
            # pprint(labels)
            print_output(data_input, statistics, pattern, label, feature)
    return labels



def make_word(chunk, alphabet, distribution, x_grid):
        s_a_x = sax(alphabet, 3, distribution, x_grid)
        word = s_a_x.sax(chunk)
        return word


def print_output(data_input, statistics, pattern, label, feature):
    print "##############################"
    print "Input Data for feature %s:" % feature
    pprint(data_input)
    print "Statistics:"
    pprint(statistics[feature])
    print "Pattern:"
    pprint(pattern)
    print "Labels:"
    pprint(label)

if __name__ == '__main__':
    time_format = '%Y-%m-%dT%H'
    alphabets = {'avgSpeed':['a', 'b', 'c'], 'vehicleCount':['d', 'e', 'f']}
    main_path = os.path.join('..', 'Analysis', 'single traffic')
    file_name = 'trafficData187430.csv'
    stream, features = read_in_stream(main_path, file_name)
    pprint(features)
    rules = {}
    rules['avgSpeed'] = GenericRule(30, 50, 'avgSpeed', len(alphabets['avgSpeed']))
    rules['vehicleCount'] = GenericRule(5, 15, 'vehicleCount', len(alphabets['vehicleCount']))

    start = datetime.strptime('2014-08-03T15', time_format)
    for i in range(500):
        start = start + timedelta(hours=1)
        distribution_start = start - timedelta(hours=3)
        duration = 1
        end = start + timedelta(hours=1)
        distributions = {}
        x_grids = {}
        try:
            for feature in ['avgSpeed']:#features:
                distribution, x_grid = stream.get_pdf_of_time_window(feature, distribution_start, end)
                distributions[feature] = distribution
                x_grids[feature] = distribution
            extractLabelsToDocument(start, duration, stream, distributions, x_grids, rules, alphabets, prnt=True)
        except:
            continue