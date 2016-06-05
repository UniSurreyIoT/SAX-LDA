from datetime import datetime
import json
import os
import itertools
from pprint import pprint

import gensim

from PyQt4.QtCore import SIGNAL
import numpy

from corpus import Corpus
from sax import sax
from dataimport.pandasDataWrapper import Stream
from workerThread import WorkerThread
import random
__author__ = 'daniel'

hour_day = False
average = False
model = 'lda'


def write_stats(f, weather_stats, traffic_stats):
    f.write("Statistics:\n")
    json.dump(weather_stats, f)
    f.write("\n")
    json.dump(traffic_stats, f)
    f.write("\n")


def write_initial_topics2file(current_date, doc_ldas, id2token):
    with open("document_topics.txt", "ab") as f:
        print "Topics after initial training phase\n"
        f.write("Topics after initial training phase\n")
        for new_doc_ldas in doc_ldas:
            topic_string = str(current_date) + ":"
            for tuple in new_doc_ldas:
                topic_string += "%s*%s " % (tuple[1], id2token[tuple[0]])
            # topics = reduce(lambda x, y: x+("(%s*%s)" % (id2token(y[1]), y[0])),doc_lda)
            topic_string += "\n"
            f.write(topic_string)
        f.write("Training day is over!\n")
        print "Training day is over!"


def write_new_topics2file(current_date, new_doc_ldas, id2token):
    with open("document_topics.txt", "ab") as f:
        for key, new_doc_lda in new_doc_ldas.items():
            topic_string = str(current_date) + " Sensor" + key + ":"
            for tuple in new_doc_lda:
                topic_string += "%s*%s" % (tuple[1], id2token[tuple[0]])
                # topics = reduce(lambda x, y: x+("(%s*%s)" % (id2token(y[1]), y[0])),doc_lda)
            f.write("\n")
            f.write(topic_string)


class ldaLogic(WorkerThread):
    def __init__(self, lda_config, main_data_path, context_data_path, parent_thread):
        WorkerThread.__init__(self, parent_thread)
        self.lda_config = lda_config
        self.main_data_path = main_data_path
        self.context_data_path = context_data_path
        self.context_data_path = context_data_path
        self.documents = []
        self.corp = None
        self.lda_model = None
        self.time_format = '%Y-%m-%dT%H'
        self.doc_files = {}

    def read_in_streams(self):
        self.main_streams = {}

        for file_name in os.listdir(self.main_data_path):
            if file_name.endswith('.csv'):
                self.main_streams[file_name[:-4]] = Stream(self.main_data_path, file_name)

        self.main_features = self.main_streams.values()[0].get_feature_names()

        self.context_stream = {}
        for file_name in os.listdir(self.context_data_path):
            if file_name.endswith('.csv'):
                self.context_stream = Stream(self.context_data_path, file_name)

        self.context_features = self.context_stream.get_feature_names()
        self.lda_config.set_feature_description(self.context_features + self.main_features)

        self.dictionary = self.make_dictionary()

    def make_dictionary(self):
        temp_dictionary = []
        dictionary = []
        for alphabet in self.lda_config.alphabets.values():
            for permutation in itertools.product(alphabet, repeat=self.lda_config.word_length):
                temp_dictionary.append("".join(permutation))
        if hour_day:
            hours = [str(hour) for hour in range(24)]
            day_map = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
            for word in temp_dictionary:
                for hour in hours:
                    for day in day_map:
                        dictionary.append(word+hour+day)
        elif average:
            averages = range(0, 4)
            for word in temp_dictionary:
                for avg in averages:
                    dictionary.append(word+str(avg))
        else:
            dictionary = temp_dictionary
        pprint(dictionary)
        return dictionary

    def make_context_pattern(self, stream, start, end, stats, hour, day=None):
        words = []
        for feature in self.context_features:
            alphabet = self.lda_config.alphabets[feature]
            if stats[feature]['max'] == stats[feature]['min']:
                words.extend(self.make_special_patterns(alphabet, start, end, hour, day))
                continue
            distribution, x_grid = stream.get_pdf_of_time_window(feature, start, end)
            word_start = start
            while word_start < end:
                word_end = word_start + self.lda_config.word_duration
                chunk = stream.get_time_window(feature, word_start, word_end)
                if len(chunk > 0):
                    words.append(self.make_pattern(chunk, alphabet, distribution, x_grid, hour, day))
                word_start += self.lda_config.word_duration
        return words

    def make_main_patterns(self, stream, start, end, stats, sensor_id, hour, day=None):
        words = []
        for feature in self.main_features:
            alphabet = self.lda_config.alphabets[feature]
            if stats[sensor_id][feature]['max'] == stats[sensor_id][feature]['min']:
                words.extend(self.make_special_patterns(alphabet, start, end, hour, day))
                continue
            distribution, x_grid = stream.get_pdf_of_time_window(feature, start, end)
            word_start = start
            while word_start < end:
                word_end = word_start + self.lda_config.word_duration
                chunk = stream.get_time_window(feature, word_start, word_end)
                words.append(self.make_pattern(chunk, alphabet, distribution, x_grid, hour, day))
                word_start += self.lda_config.word_duration
        return words

    def make_special_patterns(self, alphabet, start, end, hour, day=None):
        words = []
        while start < end:
            if hour_day:
                words.append(alphabet[0]+hour+day)
            else:
                words.append(alphabet[0])
            start += self.lda_config.word_duration
        return words

    def make_pattern(self, chunk, alphabet, distribution, x_grid, hour, day=None):
        s_a_x = sax(alphabet, self.lda_config.word_length, distribution, x_grid)
        if hour_day:
            word = s_a_x.sax(chunk)+hour+day
        elif average:
            avg = reduce(lambda x, y: x + y, chunk) / len(chunk)
            avg = int(avg)/50
            word = s_a_x.sax(chunk)+str(avg)
        else:
            word = s_a_x.sax(chunk)
        return word

    def save_documents_to_file(self, docs, start, end, weather_stats, traffic_stats):
        for key, doc in docs.items():
            if key not in self.doc_files.keys():
                f_name = key + ".txt"
                self.doc_files[key] = (open(f_name, "wb"))
            self.doc_files[key].write("Period: %s to %s" % (str(start), str(end)))
            json.dump(doc, self.doc_files[key])
            self.doc_files[key].write("\n")
            write_stats(self.doc_files[key], weather_stats, traffic_stats[key])


    def doWork(self):
        current_date = datetime.strptime("2014-08-03T08", self.time_format)
        end_date = datetime.strptime("2014-09-30T00", self.time_format)

        range = end_date - current_date
        max_days = int(range.days)
        days_passed = 0
        self.emit(SIGNAL("primaryText( PyQt_PyObject )"), "Days")
        self.emit(SIGNAL("secondaryText( PyQt_PyObject )"), "Hours")
        self.emit(SIGNAL("primaryRange( PyQt_PyObject )"), (0, max_days))
        self.emit(SIGNAL("secondaryRange( PyQt_PyObject )"), (0, 24))

        full_day = current_date
        hours_passed = 0
        training_end = current_date + self.lda_config.training_time
        day_map = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        while current_date < end_date:
            hour = str(current_date.hour)
            day = str(day_map[current_date.weekday()])
            if full_day.month < current_date.month or full_day.day < current_date.day:
                if hours_passed < 24:
                    self.emit(SIGNAL("secondaryValue( PyQt_PyObject )"), 23)
                    hours_passed = 0
                days_passed += 1
                self.emit(SIGNAL("primaryValue( PyQt_PyObject )"), days_passed)
                full_day = current_date
                print days_passed

            if hours_passed < current_date.hour:
                hours_passed += 1
                hours_passed %= 24
                self.emit(SIGNAL("secondaryValue( PyQt_PyObject )"), hours_passed)
                # check_current_hour = current_date.hour
                print hours_passed
            end_of_document_window_date = current_date + self.lda_config.window_size
            current_documents = {s_id: [] for s_id in self.main_streams.keys()}
            traffic_stats = {s_id: [] for s_id in self.main_streams.keys()}
            weather_stats = {
                feature: self.context_stream.get_statistics(feature, current_date, end_of_document_window_date)
                for feature in self.context_features}
            weather_words = self.make_context_pattern(self.context_stream, current_date, end_of_document_window_date,
                                                      weather_stats, hour, day)
            for sensor_id, stream in self.main_streams.items():
                current_documents[sensor_id].extend(weather_words)
                try:
                    traffic_stats[sensor_id] = {feature: stream.get_statistics(feature, current_date,
                                                                               end_of_document_window_date)
                                                for feature in self.main_features}
                    traffic_words = self.make_main_patterns(stream, current_date, end_of_document_window_date,
                                                            traffic_stats, sensor_id, hour, day)
                    current_documents[sensor_id].extend(traffic_words)
                except:
                    continue
                random.shuffle(current_documents[sensor_id])
            # pprint(current_documents)
            self.save_documents_to_file(current_documents, current_date, end_of_document_window_date, weather_stats,
                                        traffic_stats)
            if current_date < training_end:
                print "Gathering enough documents for training the model %s (end of training: %s)" \
                      % (str(current_date), str(training_end))
                self.documents.extend(current_documents.values())
                current_date += self.lda_config.window_size
                continue
            current_date += self.lda_config.window_size

            first_run = self.corp is None or self.lda_model is None
            if first_run:
                self.train_model(current_date)

            else:
                self.update_model(current_date, current_documents)

        for doc_file in self.doc_files.values():
            doc_file.close()

    def update_model(self, current_date, current_documents):
        new_docs = {key: doc for key, doc in current_documents.items()}
        new_corpus = self.corp.new_corpus(new_docs.values())
        print "updated corpus"
        try:
            print "updated model"
            if(model is 'lda'):
                self.lda_model.update(new_corpus,eval_every=len(self.corp.corpus))
            if(model is 'lsa'):
                self.lda_model.add_documents(new_corpus, chunksize=100)
        except IndexError:
            print "update failed"
        new_doc_ldas = {key: self.lda_model[self.corp.dictionary.doc2bow(new_doc)] for key, new_doc in new_docs.items()}
        print "Incoming new document and writing to log at %s" % str(current_date)
        # write_new_topics2file(current_date, new_doc_ldas, self.id2token)
        pprint(self.lda_model.print_topics(self.lda_config.num_topics))
        #
        # new_doc_ldas = {key: self.lda_model[new_doc] for key, new_doc in new_docs.items()}
        # self.lda_model.update(new_doc_ldas.values(), eval_every=len(new_doc_ldas.values()))
        # if self.perplexity_too_high(new_doc_ldas.values()):
        #     self.documents.extend(current_documents.values())
        #     self.corp = Corpus(self.documents, 'heterogeneous', self.dictionary)
        #     self.corp.initialize_corpus()
        #     self.lda_model = gensim.models.ldamodel.LdaModel(corpus=self.corp.corpus,
        #                                                  num_topics=self.lda_config.num_topics,
        #                                                  id2word=self.corp.dictionary, passes=100, eval_every=len(self.corp.corpus))
        #
        #     doc_ldas = [self.lda_model[doc_bow] for doc_bow in self.corp.corpus]
        #     id2token = self.corp.dictionary.id2token
        #     write_initial_topics2file(current_date, doc_ldas, id2token)
        # else:
        #     write_new_topics2file(current_date, new_doc_ldas.items(), id2token)

    def train_model(self, current_date):
        print "initialize corpus and lda model"
        # pprint(self.documents)
        self.corp = Corpus(self.documents, 'heterogeneous', self.dictionary)
        print "A"
        # pprint(self.corp.corpus)
        self.corp.initialize_corpus()
        print "documents"
        # pprint(self.documents)
        print "corpus"
        # pprint(self.corp.corpus)
        # initialize lda model
        # print "dictionary"
        # pprint(self.corp.dictionary)
        # print "id2token"
        # pprint(self.corp.dictionary.id2token)
        init_dictionary = self.corp.dictionary[0]
        if(model is 'lda'):
            self.lda_model = gensim.models.ldamodel.LdaModel(corpus=self.corp.corpus,
                                                             num_topics=self.lda_config.num_topics,
                                                             id2word=self.corp.dictionary.id2token, passes=100, eval_every=len(self.corp.corpus))
        if(model is 'plsa'):
            self.lda_model = gensim.models.ldamodel.LdaModel(corpus=self.corp.corpus,
                                                             num_topics=self.lda_config.num_topics,
                                                             id2word=self.corp.dictionary.id2token, passes=100, eval_every=len(self.corp.corpus),
                                                             alpha=1, eta=1)
        if(model is 'lsa'):
            self.lda_model = gensim.models.LsiModel(corpus=self.corp.corpus, num_topics=self.lda_config.num_topics,
                                                id2word=self.corp.dictionary.id2token, chunksize=100)
        # print "C"
        # doc_ldas = [self.lda_model[doc_bow] for doc_bow in self.corp.corpus]
        # print "z-space"
        # pprint(doc_ldas)
        # print "Token"
        self.id2token = self.corp.dictionary.id2token
        # pprint(self.id2token)
        print "Initial Topics"
        pprint(self.lda_model.print_topics(self.lda_config.num_topics))
        # write_initial_topics2file(current_date, doc_ldas, self.id2token)

    def test_with_old_docs(self, docs, id2token):
        for i, doc in enumerate(docs):
            print "document %i" %i
            for tuple in doc:
                print "%s*%s" % (tuple[1], id2token[tuple[0]])
        self.perplexity_too_high(docs)

    def perplexity_too_high(self, chunk):
        sample_ratio = subsample_ratio = 1.0 * len(self.documents) / len(chunk)
        corpus_words = sum(cnt for document in chunk for _, cnt in document)
        print "Number of words: %i, number of documents: %i" % (corpus_words, len(chunk))

        print "Sample ratio: %f" % sample_ratio
        perwordbound = self.lda_model.log_perplexity(chunk, total_docs=len(self.documents), logging=False)
        perplexity = numpy.exp2(-perwordbound)
        print "%.3f per-word bound, %.1f perplexity estimate based on a held-out corpus of %i documents with %i words" % \
              (perwordbound, numpy.exp2(-perwordbound), len(chunk), len(self.corp.corpus))
        if perplexity > 1000:
            return True
        return False
