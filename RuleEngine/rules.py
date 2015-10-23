import pprint

__author__ = 'Daniel Puschmann'


def directions_of_pattern(pattern):
    #TODO make sure this makes sense
    if all([pattern[i] ==pattern[i-1] for i in range(1, len(pattern))]):
        return 'remaining'
    elif all([pattern[i] >=pattern[i-1] for i in range(1, len(pattern))]):
        return 'decreasing'
    elif all([pattern[i] <=pattern[i-1] for i in range(1, len(pattern))]):
        return 'increasing'
    else:
        return 'alternating'

def range_in_pattern(pattern):
    return ord(max(pattern))-ord(min(pattern))

def distance_in_pattern(pattern):
    distances = {0:'no', 1:'slight', 2:'little', 3:'medium', 4:'big'}
    d = range_in_pattern(pattern)
    try:
        distance = distances[d]
    except:
       raise Exception('Check the alphabet size! (pattern: %s, distance: %i)' % (pattern, d))
    return distance


class GenericRule(object):

    def __init__(self, lda_config):
        self.lda_config = lda_config

    def apply_rule(self, pattern, stats):
        if pattern.startswith('special'):
            value = pattern[pattern.find('special')+1:]
            return Label('remaining', 0, value, value, pattern, 'unknown')
        dir = directions_of_pattern(pattern)
        dist = distance_in_pattern(pattern)
        feature = self.get_feature_from_pattern(pattern)
        min_val = stats[feature]['min']
        max_val = stats[feature]['max']
        label = Label(dir, dist, min_val, max_val, pattern, feature)
        return label


    def get_feature_from_pattern(self, pattern):
        for feature, alphabet in self.lda_config.alphabets.items():
            if pattern[0] in alphabet:
                return feature
        pprint(self.lda_config.alphabets)
        raise Exception('Pattern with unknown alphabet (Pattern: %s)' % pattern)

class ExplicitRule(object):

    #list of patterns, dict of stats, each stat is tuple/list of size one or two
    def __init__(self, patterns, stats, label):
        for key, stat in stats.items():
            if len(stat) > 2:
                raise Exception("Invalid Restrictions for %s" % key)
        self.patterns = patterns
        self.stats = stats
        self.label = label

    def apply_rule(self, patterns, stats):
        if all(pattern not in self.patterns for pattern in patterns):
            #rule does not apply because pattern don't belong
            return None
        elif not all(self.valid_stats_for_rule(key, stat) for key, stat in stats.items()):
            #rule does not apply because statistics don't fullfill condition
            return None
        else:
            # rule does apply
            return self.label

    def valid_stats_for_rule(self, key, statistic):
        if len(self.stats[key] == 0):
            #no restrictions for this feature
            return True
        elif len(self.stats[key] == 1):
            #stat has to be exactly the value
            return self.stats[key][0] == statistic
        elif self.stats[key][0] is None:
            #left open range
            return statistic < self.stats[key][1]
        elif self.stats[key][1] is None:
            #right open range
            return self.stats[key][0] < statistic
        else:
            #closed range
            return self.stats[key][0] < statistic < self.stats[key][1]

class Label(object):

    def __init__(self, label_name, description, min_val, max_val, pattern, feature=None):
        self.label = label_name
        self.description = description
        self.feature = feature
        self.min = min_val
        self.max = max_val
        self.pattern = pattern

    def toString(self):
        if self.feature is not None:
            return 'Label: %s \n' \
                   'Description: %s \n' \
                   'Feature: %s \n' \
                   'Range: (%i, %i)' % (self.label, self.description, self.feature, self.min, self.max)
        else:
            return 'Label: %s \n' \
                   'Description: %s \n' \
                   'Range: (%i, %i)' % (self.label, self.description, self.min, self.max)