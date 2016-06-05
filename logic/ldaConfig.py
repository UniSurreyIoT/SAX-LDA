import datetime
from pprint import pprint
import string

__author__ = 'Daniel Puschmann'

def make_alphabets(feature_descriptions, alphabet_size):
    print "making alphabet with size %i" %alphabet_size
    alphabet_start = 0
    alphabets = {}
    print "features"
    pprint(feature_descriptions)
    for k in feature_descriptions:
        if k == 'TIMESTAMP':
            continue
        alphabet = string.ascii_letters[alphabet_start:alphabet_start+alphabet_size]
        alphabets[k] = alphabet
        alphabet_start += alphabet_size
    print "alphabets"
    pprint(alphabets)
    return alphabets

class LdaConfig(object):

    def __init__(self, feature_names, num_topics=100, training_time=1,
                 word_length=3, word_duration=1,
                 windows_size=4,
                 distribution_window_size=4, alphabet_size=5):
        self.alphabet_size = alphabet_size
        self.word_length = word_length
        self.window_size = datetime.timedelta(hours=windows_size)
        if feature_names is not None:
            self.alphabets = make_alphabets(feature_names, self.alphabet_size)
        self.data_path = "C:\Users\dp00143\Dropbox\SurreyBackup\LDAPlusPlus\data\Analysis\\"
        self.num_topics = num_topics
        self.document_file = open("document_topics.txt", "wb")
        self.training_time = datetime.timedelta(hours=training_time)
        self.word_duration = datetime.timedelta(hours=word_duration)
        self.distribution_window_size = datetime.timedelta(hours=distribution_window_size)


    def set_feature_description(self, feature_names):
        self.alphabets = make_alphabets(feature_names, self.alphabet_size)
