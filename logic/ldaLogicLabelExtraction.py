__author__ = 'Daniel Puschmann'

from pprint import pprint, pformat

import numpy
from PyQt4.QtCore import SIGNAL

from RuleEngine.extractLabels import extractLabelsToDocument
from RuleEngine.genericRule import GenericRule
from RuleEngine.label import Label
from lda_logic import ldaLogic
from metrics import f_measure, final_measure


class ldaLogicLabels(ldaLogic):

    def __init__(self, lda_config, main_data_path, context_data_path, parent_thread):
            ldaLogic.__init__(self, lda_config, main_data_path, context_data_path, parent_thread)
            self.make_rules()


    def make_rules(self):
        self.rules = {}
        self.rules['avgSpeed'] = GenericRule(30, 50, 'avgSpeed', self.lda_config.alphabet_size)
        self.rules['vehicleCount'] = GenericRule(5, 15, 'vehicleCount', self.lda_config.alphabet_size)
        self.rules['wspdm'] = GenericRule(10,20, 'wspdm', self.lda_config.alphabet_size)
        self.rules['tempm'] = GenericRule(10,20, 'tempm', self.lda_config.alphabet_size)
        self.held_out_features = []



    def make_dictionary(self):
        levels = ["Low", "Medium", "High"]
        features = self.main_features + self.context_features
        modifiers = ["slowly", "rapidly"]
        pattern_movements = ["steady", "downward_peak", "upward_peak", "increasing", "decreasing"]

        dictionary = []
        for level in levels:
            for feature in features:
                for modifier in modifiers:
                    for pattern_movement in pattern_movements:
                        if pattern_movement not in ["steady", "downward_peak", "upward_peak"]:
                            label = Label(level, feature, modifier, pattern_movement)
                            dictionary.append(str(label))

        for level in levels:
            for feature in features:
                    for pattern_movement in pattern_movements:
                        label = Label(level, feature, None, pattern_movement)
                        dictionary.append(str(label))
        pprint(dictionary)
        return dictionary

    def doWork(self):
        current_date = self.main_streams.values()[0].get_start_date()
        end_date = self.main_streams.values()[0].get_end_date()

        time_range = end_date - current_date
        max_days = int(time_range.days)
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
            day = str()
            if full_day.month < current_date.month or full_day.day < current_date.day:
                if hours_passed < 24:
                    self.emit(SIGNAL("secondaryValue( PyQt_PyObject )"), 23)
                    hours_passed = 0
                days_passed += 1
                self.emit(SIGNAL("primaryValue( PyQt_PyObject )"), days_passed)
                full_day = current_date
                # print days_passed

            if hours_passed < current_date.hour:
                hours_passed += 1
                hours_passed %= 24
                self.emit(SIGNAL("secondaryValue( PyQt_PyObject )"), hours_passed)
                # check_current_hour = current_date.hour
                # print hours_passed

            context_distributions = {}
            context_grids = {}
            distribution_start = current_date-self.lda_config.distribution_window_size
            current_end = current_date+self.lda_config.word_duration
            for feature in self.context_features:
                try:
                    dist, grid = self.context_stream.get_pdf_of_time_window(feature, distribution_start, current_end)
                    context_distributions[feature] = dist
                    context_grids[feature] = grid
                except numpy.linalg.linalg.LinAlgError as err:
                    print "Error occurred in feature %s at %s: %s" % (feature, current_date, err.message)
            current_documents = {s_id: [] for s_id in self.main_streams.keys()}

            context_labels = extractLabelsToDocument(current_date,  self.lda_config.word_duration, self.context_stream,
                                                     context_distributions, context_grids, self.rules,
                                                     self.lda_config.alphabets)

            for sensor_id, stream in self.main_streams.items():
                current_documents[sensor_id].extend(context_labels)
                main_distributions = {}
                main_grids = {}
                for feature in self.main_features:
                    try:
                        dist, grid = self.main_streams[sensor_id].get_pdf_of_time_window(feature, distribution_start,
                                                                                         current_end)
                        main_distributions[feature] = dist
                        main_grids[feature] = dist
                    except numpy.linalg.linalg.LinAlgError as err:
                        print "Error occurred in feature %s at %s: %s" % (feature, current_date, err.message)
                main_labels = extractLabelsToDocument(current_date, self.lda_config.word_duration,
                                                          self.main_streams[sensor_id], main_distributions, main_grids,
                                                          self.rules, self.lda_config.alphabets)
                current_documents[sensor_id].extend(main_labels)

            #TODO save the labels to a file

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
                held_out_feature = 'avgSpeed'
                self.predict_docs(held_out_feature, current_date, current_documents, metric=f_measure)

                # self.predict_single_word_documents()
                # for doc_file in self.doc_files.values():
                #     doc_file.close()
                # return
                # self.update_model(current_date, current_documents)
        print "Experiment finished"
        final_measure()
        for doc_file in self.doc_files.values():
            doc_file.close()

    def predict_single_word_documents(self):
        for label in self.dictionary:
            single_word_document = [label]
            single_word_topic = self.lda_model[self.corp.dictionary.doc2bow(single_word_document)]

            print "##############################"
            print "Document:"
            pprint(single_word_document)
            print "Predicted topic:"
            pprint(self.lda_model.print_topic(max(single_word_topic, key=lambda item: item[1])[0]))
            # pprint(single_word_topic)

    def predict_docs(self, held_out_feature, current_date, current_documents, write_to_log=True, metric=None):

        new_docs = {key: doc for key, doc in current_documents.items()}
        new_corpus = self.corp.new_corpus(new_docs.values())

        covered_docs = {key: [word for word in doc if held_out_feature not in word] for key, doc in current_documents.items()}
        # new_doc_ldas = {key: self.lda_model[self.corp.dictionary.doc2bow(new_doc)] for key, new_doc in new_docs.items()}
        covered_doc_ldas = {key: self.lda_model[self.corp.dictionary.doc2bow(new_doc)] for key, new_doc in new_docs.items()}
        actual_labels = []
        predicted_labels = []
        found_labels = set()
        with open("label_predictions.txt", "ab") as label_file:
            for key, topic in covered_doc_ldas.items():
                if write_to_log:
                    label_file.write("##############################")
                    label_file.write("Actual document %s at %s:" % (key, str(current_date)))
                    label_file.write(pformat(new_docs[key]))
                    label_file.write("Covered document:")
                    label_file.write(pformat(covered_docs[key]))
                    label_file.write("Predicted topic:")
                    label_file.write(pformat(self.lda_model.print_topic(max(topic, key=lambda item: item[1])[0])))

                predicted_topic = self.lda_model.show_topic(max(topic, key=lambda item: item[1])[0])
                tmp = [word for (_, word) in predicted_topic if held_out_feature in word]
                tmp.append("No_Prediction")
                actual_label = [word for word in new_docs[key] if held_out_feature in word]
                predicted_label = tmp[0]
                # print "predicted"
                # pprint(predicted_label)
                # print "actual"
                # pprint(actual_label)
                if len(actual_label) == 0:
                    print "no documents at time: %s" % str(current_date)
                    pprint(current_documents)
                else:
                    actual_labels.append(actual_label[0])
                    predicted_labels.append(predicted_label)
                    found_labels.add(actual_label[0])
            if metric is not None:
                # pprint(found_labels)
                metric(actual_labels, predicted_labels, current_date, current_documents, held_out_feature, found_labels)

            try:
                print "updated model"
                self.lda_model.update(new_corpus, eval_every=len(self.corp.corpus))
            except IndexError:
                print "update failed"




