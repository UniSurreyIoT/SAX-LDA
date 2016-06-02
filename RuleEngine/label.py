__author__ = 'Daniel Puschmann'


class Label(object):

    def __init__(self, level=None, feature=None, modifier=None, pattern_movement=None):
        self.level = level
        self.feature = feature
        self.modifier = modifier
        self.pattern_movement = pattern_movement

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.modifier is None:
            return "%s_%s_%s" % (self.level, self.feature, self.pattern_movement)
        else:
            return "%s_%s_%s_%s" % (self.level, self.feature, self.modifier, self.pattern_movement)
