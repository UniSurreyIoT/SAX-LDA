import numpy as np

from logic import paa

__author__ = 'Daniel Puschmann'


class sax(object):


    def __init__(self, alphabet, word_length, pdf, x_grid):
        self.alphabet = alphabet
        self.p = paa(word_length)
        self.betas = self.calculate_betas_custom_distribution(pdf, x_grid)

    def find_beta_index(self, betas, section_mean):
        for i, beta in enumerate(betas):
            if section_mean < beta:
                return i
        return i

    def normalize(self, data):
        data2 = np.array(data)
        data2 -= (np.mean(data))
        data2 *= (1.0/data2.std())
        return data2

    def sax(self, data):
        locations = []
        reduced_data = self.p.paa(data)
        for section_mean in reduced_data:
            beta_index = self.find_beta_index(self.betas, section_mean)
            locations.append(beta_index)
        word = ''.join([self.alphabet[ind] for ind in locations])
        return word

    def sax_reduced_data(self, reduced_data):
        locations = []
        for section_mean in reduced_data:
            beta_index = self.find_beta_index(self.betas, section_mean)
            locations.append(beta_index)
        word = ''.join([self.alphabet[ind] for ind in locations])
        return word

    def calculate_betas_custom_distribution(self, pdf, x_grid):
        norm_constant = sum(pdf)
        # normalize values so they are between 0 and 1
        pdf = [float(x)/float(norm_constant) for x in pdf]
        s = 0
        alphabet_size = len(self.alphabet)
        quantile = 1./(alphabet_size)
        betas = []
        for i, v in enumerate(pdf):
            s += v
            if s >= quantile:
                betas.append(x_grid[i])
                quantile = float(len(betas)+1)/ alphabet_size
                if quantile == 1:
                    break
        return betas


def normalize(data):
        data2 = np.array(data)
        data2 -= (np.mean(data))
        data2 *= (1.0/data2.std())
        return data2


# means = [normalize([223]), normalize([13]), normalize([100230]), normalize([-213]), normalize([3]), ]
#
# pprint(means)
