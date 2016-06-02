__author__ = 'Daniel Puschmann'

from label import Label

def range_in_pattern(pattern):
    return ord(max(pattern))-ord(min(pattern))

def distance_in_pattern(pattern, alphabet_size=5):
    if alphabet_size == 5:
        distances = {0:'', 1:'slowly_', 2:'', 3:'', 4:'rapidly_'}
    elif alphabet_size == 4:
        distances = {0:'', 1:'slowly_', 2:'', 3:'rapidly_'}
    elif alphabet_size == 3:
        distances = {0:'', 1:'slowly_', 2:'rapidly_'}
    else:
        raise Exception('Alphabet size of %i is currently not supported!' % alphabet_size)
    d = range_in_pattern(pattern)
    try:
        distance = distances[d]
    except:
       raise Exception('Check the alphabet size! (pattern: %s, distance: %i)' % (pattern, d))
    return distance


class GenericRule(object):

    def __init__(self, low_threshold, high_threshold, feature, alphabet_size):
        self.alphabet_size = alphabet_size
        assert low_threshold<high_threshold, "Low threshold has to be lower than high threshold"
        self.low = low_threshold
        self.high = high_threshold
        self.feature = feature
        self.level = None
        self.modifier = None
        self.pattern_movement = None

    def apply(self, pattern, statistics):
        min_value, max_value, average_value = statistics[self.feature]['min'], statistics[self.feature]['max'], \
                                              statistics[self.feature]['mean']
        self.evaluate_level(average_value)
        self.evaluate_pattern(pattern, min_value, max_value)
        label = Label(level=self.level, feature=self.feature, modifier=self.modifier,
                      pattern_movement=self.pattern_movement)
        return label

    def evaluate_level(self, average_value):
        if average_value < self.low:
            self.level = 'Low'
        elif average_value > self.high:
            self.level = 'High'
        else:
            self.level = 'Medium'

    def evaluate_pattern(self, pattern, min_value, max_value):
        dist = distance_in_pattern(pattern, alphabet_size=self.alphabet_size)
        if all([pattern[i] ==pattern[i-1] for i in range(1, len(pattern))]):
            self.pattern_movement = 'steady'
        elif all([pattern[i] >=pattern[i-1] for i in range(1, len(pattern))]):
            self.pattern_movement = '%sincreasing' % dist
        elif all([pattern[i] <=pattern[i-1] for i in range(1, len(pattern))]):
            self.pattern_movement = '%sdecreasing' % dist
        elif has_downward_peak(pattern):
            self.pattern_movement = 'downward_peak'
        elif has_upward_peak(pattern):
            self.pattern_movement = 'upward_peak'

def has_downward_peak(pattern):
    going_down = pattern[0]>pattern[1]
    if not going_down:
        return going_down
    for i in range(0, len(pattern)-1):
        if going_down:
            if pattern[i]<pattern[i+1]:
                going_down = False
            else:
                continue
        else:
            if pattern[i]<pattern[i+1]:
                continue
            else:
                return False
    return not going_down



def has_upward_peak(pattern):
    going_up = pattern[0]<pattern[1]
    if not going_up:
        return going_up
    for i in range(0, len(pattern)-1):
        if going_up:
            if pattern[i]>pattern[i+1]:
                going_up = False
            else:
                continue
        else:
            if pattern[i]>pattern[i+1]:
                continue
            else:
                return False
    return not going_up