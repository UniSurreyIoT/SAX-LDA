from pprint import pprint

__author__ = 'Daniel Puschmann'
from gensim import corpora

class Corpus(object):

    def __init__(self, documents, source, dictionary):
        self.all_tokens = sum(documents, [])
        pprint(self.all_tokens)
        #remove words which only appear once in the whole corpus
        # self.token_once = set(word for word in set(self.all_tokens) if self.all_tokens.count(word) == 1)
        # pprint(self.token_once)
        # self.documents = [[word for word in sax_representation if word not in self.token_once]
        #                   for sax_representation in documents]
        self.documents = documents
        self.dictionary = corpora.Dictionary([dictionary])
        self.dictionary.save(source+".dict")
        self.corpus = [self.dictionary.doc2bow(document, allow_update=False) for document in self.documents]
        self.source = source


    def new_corpus(self, documents):
        new_corpus = []
        for document in documents:
            self.all_tokens += document
            self.token_once = set(word for word in set(self.all_tokens) if self.all_tokens.count(word) == 1)
            new_document = [word for word in document if word not in self.token_once]
            new_corpus += [self.dictionary.doc2bow(new_document, allow_update=False)]
        return new_corpus


    def initialize_corpus(self):
       corpora.MmCorpus.serialize(self.source+".mm", self.corpus)