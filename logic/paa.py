__author__ = 'Daniel Puschmann'

import numpy as np
import bottleneck as bn
import math
class paa(object):

    def __init__(self, word_length):
        self.word_length = word_length

    def paa(self, data_slice):
        if self.word_length > len(data_slice):
            data = data_slice.values.tolist()
            for i in range(len(data), self.word_length):
                data.append(bn.nanmean(data[:i-1]))
                if(math.isnan(data[i])):
                    data[i] = 0
            return np.array(data)
        if self.word_length == len(data_slice):
            return data_slice
        data = np.array_split(data_slice, self.word_length)
        result = []
        for section in data:
            if math.isnan(bn.nanmean(section)):
                result.append(0)
            else:
                result.append(bn.nanmean(section))
        result = np.array(result)
        return result
