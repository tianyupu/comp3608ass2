#!/usr/bin/python

import os, os.path
import gzip
import random
import datetime
from preprocessor import *
from classifier import *

SUBJ_FNAME = 'subject_test.csv'
BODY_FNAME = 'body_test.csv'

def cross_validation(source_dir, subsets, nfeatures)
    for index in subsets:
        training_set = subsets[:index] + subsets[index:]
        validation_set = subsets[index]
        subj_corp, body_corp = preprocess_subset(source_dir, training_set)
        #feature selection
        subj_sel = feature_select(subj_corp, 'df', nfeatures)
        body_sel = feature_select(body_corp, 'df', nfeatures)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        #feature weighing
        write_dataset(subj_sel, directory, now + SUBJ_FNAME)
        write_dataset(body_sel, directory, now + BODY_FNAME)
        #build then train the classifier
        subj_classifier = Classifier(SUBJ_FNAME)
        body_classifier = Classifier(BODY_FNAME)
        subj_classifier.train()
        body_classifier.train()
        #test each example in training set
        subj_correct = 0
        body_correct = 0
        for f in training_set:
            path = os.path.join(source_dir, f)
            src_f = gzip.open(path)
            content_lines = content.split('\n', 1) # first line is always subject, rest is body
            subj, body = content_lines[0].strip(), content_lines[1].strip()
            
def preprocess_subset(source_dir, subset)
    """Preprocess the files in subset in the directory source_dir.

    Returns the two corpora as a 2-tuple."""
    subj_corp = Corpus()
    body_corp = Corpus()

    for f in subset:
        path = os.path.join(source_dir, f)
        src_f = gzip.open(path)
        content = src_f.read()
        content_lines = content.split('\n', 1) # first line is always subject, rest is body
        subj, body = content_lines[0].strip(), content_lines[1].strip()
        subj = subj.lstrip('Subject: ') # strip away the word subject
        # add the contents of the file just read to the corpus
        subj_corp.add(subj, f)
        body_corp.add(body, f)
        src_f.close()
    return subj_corp, body_corp

def get_validationsets(source_dir, folds):
    src_files = os.listdir(source_dir)
    spam_files = []
    nonspam_files = []
    for f in src_files:
        if 'spmsg' in f:
            spam_files.append(f)
        else:
            nonspam_files.append(f)
    spam_partitions = random_partition(spam_files, folds)
    nonspam_partitions = random_partition(nonspam_files, folds)
    validation_sets = []
    for i in xrange(folds):
        validation_sets.append([])
        validation_sets[i].extend(spam_partitions[i])
        validation_sets[i].extend(nonspam_partitions[i])
        random.shuffle(validation_sets[i])
    return validation_sets
    
##def random_partition(superset, k):
##    """Randomly partition superset into k subsets such that the lengths of no
##    two subsets differ in length by more than 1"""
##
##    N = len(superset)
##    n = N/k
##
##    #assign the k subsets n elements each
##    subsets = []
##    for i in xrange(k):
##        #randomly choose n elements from superset and append to a subset
##        subsets.append([])
##        rand_indices = random.sample(range(len(superset)), n)
##        for rand_index in rand_indices:
##            subsets[i].append(superset[rand_index])
##        #remove the n elements from superset so they are not chosen again
##        for index in sorted(rand_indices, reverse=True):
##            superset.pop(index)
##
##    #now randomly assign the remaining elements in the superset to the subsets
##    remaining = N - n
##    for i in xrange(k):
##        #if there are no elements left in the superset, then we are done
##        if len(superset) == 0:
##            break
##        rand_index = random.randint(0, len(superset) - 1)
##        subsets[i].append(superset[rand_index])
##        superset.pop(rand_index)
##
##    return subsets

def random_partition(superset, k):
    """Randomly partition superset into k subsets such that the lengths of no
    two subsets differ in length by more than 1"""

    N = len(superset)
    subsets = [[] for i in xrange(k)]

    #main loop to assign every element in superset
    for i in xrange(N):
        for j in xrange(k):
            if len(superset) == 0:
                break
            rand_index = random.randint(0, len(superset) - 1)
            subsets[j].append(superset[rand_index])
            superset.pop(rand_index)
    return subsets
