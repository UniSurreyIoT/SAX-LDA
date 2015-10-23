import datetime
import os
# from pandas import json
from RuleEngine.rules import ExplicitRule, GenericRule
from logic.ldaConfig import LdaConfig
from json import dumps, loads, JSONEncoder

__author__ = 'Daniel Puschmann'


explicit_rules = []
generic_rule = None

# feature names and corresponding alphabet size
feature_descriptions = {'vehicleCount': 5, 'avgSpeed': 5, 'tempm': 5, 'wspdm': 5}#'rain': 2,
feature_names = feature_descriptions.keys()

lda_config = LdaConfig(feature_names=feature_descriptions, windows_size=datetime.timedelta(hours=8),
                       distribution_window_size=datetime.timedelta(hours=8))
def define_rule(patterns, stats, label):
    explicit_rules.append(ExplicitRule(patterns, stats, label))



generic_rule = GenericRule(lda_config)
def apply_rules(document):
    patterns = document['patterns']
    stats = document['statistics']
    period = document['period']
    labels = []
    for pattern in patterns:
        labels.append(generic_rule.apply_rule(pattern, stats))
    for rule in explicit_rules:
        labels.append(rule.apply_rule())
    return {period: labels}

def read_documents(file_name):
    documents = []
    with open(file_name, "rb") as f:
        for line in f:
            if line.startswith('Period'):
                period = line[line.find(': ')+1:line.find('[')]
                patterns = line[line.find('[')+1:line.find(']')].replace('"', '').split(", ")
                # print period
                # print patterns
            elif line.startswith('{"wspdm"'):
                weather_statistics = loads(line.replace('NaN', '0'))
                # print weather_statistics
            elif line.startswith('{"vehicleCount"'):
                try:
                    traffic_statistics = loads(line.replace('NaN', '0').replace('\x00','').replace('\n', ''))
                except Exception:
                    print repr(line.replace('NaN', '0').replace('\x00','').replace('\n', ''))
                    # print repr(statistics)
                    # print repr(patterns)
                    # print repr(period)
                    raise Exception
                statistics = {key: value for (key, value) in (traffic_statistics.items() + weather_statistics.items())}
                documents.append({'period': period, 'statistics': statistics, 'patterns': patterns})

                # print traffic_statistics
    return documents

output_file_base = 'C:\Users\dp00143\Dropbox\SurreyBackup\LDAPlusPlus\Results\Labels\%s\labels%s.txt'
input_dir_base = 'C:\Users\dp00143\Dropbox\SurreyBackup\LDAPlusPlus\Results\BigDataset\%s\documents\\'
# configurations = ['Configuration %s' % letter for letter in string.ascii_uppercase[:4]]
configurations = ['Configuration E']
print configurations

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def label_documents(file_name, id, config):
    documents = read_documents(file_name)
    labels = []
    for document in documents:
        labels.append(apply_rules(document))
    with open(output_file_base % (config, id), 'wb') as f:
        for label in labels:
            js =dumps(label,cls=MyEncoder)
            f.write(js)
            f.write('\n')

for config in configurations:
    input_dir = input_dir_base %config
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.txt'):
            id = file_name[file_name.find('labels')+1:file_name.find('.txt')]
            'labeling documents for %s' % file_name
            label_documents(input_dir+file_name, id, config)

# define_rules()