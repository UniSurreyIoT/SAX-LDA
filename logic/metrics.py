__author__ = 'Daniel Puschmann'
import numpy as np
from pprint import pprint

rel_docs, ret_labels, rel_ret_labels = {}, {}, {}


def f_measure(actual_labels, predicted_labels, current_date, documents, held_out_feature, found_labels, beta=1):
    assert len(actual_labels) == len(predicted_labels), \
           "The number of predicted labels was not the number of actual labels"
    for label in found_labels:
        if label not in rel_docs.keys():
            rel_docs[label] = 0
            ret_labels[label] = 0
            rel_ret_labels[label] = 0
        with open('%sf_measure.txt' % label, 'ab') as f:
            actual_labels = np.array(actual_labels)
            predicted_labels = np.array(predicted_labels)
            relevant_documents = len(actual_labels[actual_labels==label])
            retrieved_documents = len(predicted_labels[predicted_labels==label])
            relevant_retrieved_documents = len([0 for actual_label, predicted_label in zip(actual_labels, predicted_labels)
                                       if actual_label==predicted_label and actual_label==label])
            f.write('Time %s\n' % str(current_date))
            f.write('How often did the label appear in the actual data: %i\n' % relevant_documents)
            f.write('How often was the label predicted: %i\n' % retrieved_documents)
            f.write('How often was the label correctly predicted: %i\n' % relevant_retrieved_documents)
            if retrieved_documents is 0 or relevant_retrieved_documents is 0 or relevant_documents is 0:
                p = 0
                r = 0
                f1 = 0
            else:
                p = float(relevant_retrieved_documents)/float(retrieved_documents)
                r = float(relevant_retrieved_documents)/float(relevant_documents)
                f1 = (1.0+beta**2.0)*((p*r)/((beta**2.0)*p+r))
            rel_docs[label] += relevant_documents
            ret_labels[label] += retrieved_documents
            rel_ret_labels[label] += relevant_retrieved_documents

            f.write('Precision: %f\n' % p)
            f.write('Recall: %f\n' % r)
            f.write("Resulting f%i-score: %f\n" % (beta, f1))


def final_measure(beta=1):
    pprint(rel_docs)
    with open('EndResultFMeasure.txt', 'ab') as f:
        for label in rel_docs:
            f.write("Score for label %s" % label)
            f.write('How often did the label appear in the actual data: %i\n' % rel_docs[label])
            f.write('How often was the label predicted: %i\n' % ret_labels[label])
            f.write('How often was the label correctly predicted: %i\n' % rel_ret_labels[label])
            if rel_docs[label] is 0 or ret_labels[label] is 0 or rel_ret_labels[label] is 0:
                p, r, f1 = 0, 0, 0
            else:
                p = float(rel_ret_labels[label])/float(ret_labels[label])
                r = float(rel_ret_labels[label])/float(rel_docs[label])
                f1 = (1.0+beta**2.0)*((p*r)/((beta**2.0)*p+r))
            f.write('Precision: %f\n' % p)
            f.write('Recall: %f\n' % r)
            f.write("Resulting f%i-score: %f\n" % (beta, f1))

