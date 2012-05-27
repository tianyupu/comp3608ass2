#!/usr/bin/python

import os, os.path
import gzip
import random
import datetime
import string
from preprocessor import *
from classifier import *

def cross_validation(csv_fname, folds):
  """Runs n-fold validation on the examples (each example is a weighted feature
  list) in a csv file. folds = number of folds"""
  
  # read csv file and extract lines
  f_handle = open("results/"+csv_fname, 'rU')
  lines = [line.strip() for line in f_handle.readlines()]
  header_str = lines[0]
  f_handle.close()
  # create stratified subsets. don't use the first line. It is the header
  subsets = get_validationsets(lines[1:], folds)

  # list to store the classifier accuracy for each fold
  results = []
  for index in range(len(subsets)):
    
    validation_set = subsets[index]
    training_set = subsets[:index] + subsets[index + 1:]
    # flatten the training set into a list of stringss
    training_set = [item for subset in training_set for item in subset]
    
    # output a csv file for each validation fold
    test_fname = "validation/test_"+str(index)+csv_fname
    out_f = open(test_fname, 'w')
    out_f.write(header_str+"\n"+ string.join([(line+"\n") for line in training_set]))
    out_f.close()

    # make the classifier
    classifier = Classifier(test_fname)
    classifier.train()
    # test each example in validation set
    correct = 0
    for line in validation_set:
        if classifier.test_example(line.strip()):
            correct += 1
    accuracy = float(correct)*100/len(validation_set)
    print "Accuracy: " + str(accuracy) +"%"
    results.append(accuracy)
  print "Overall accuracy: " + str(results.append(accuracy))
  return sum(results)/folds
              
def get_validationsets(lines, folds):
  """Returns a randomly stratified n-fold sample of a list of lines"""
  spam_lines = []
  nonspam_lines = []
  # split files into spam or nonspam
  for line in lines:
    if 'nonspam' in line:
      nonspam_lines.append(line)
    else:
      spam_lines.append(line)
      
  # make a random partition of spam
  spam_partitions = random_partition(spam_lines, folds)
  # make a random partition of nonspam
  nonspam_partitions = random_partition(nonspam_lines, folds)
  validation_sets = []
  
  # combining the two random partitions ensures the validation sets are
  # properly stratified.
  for i in xrange(folds):
    validation_sets.append([])
    validation_sets[i].extend(spam_partitions[i])
    validation_sets[i].extend(nonspam_partitions[folds - i - 1])
    random.shuffle(validation_sets[i])
  return validation_sets
  
def random_partition(superset, k):
  """Randomly partition superset into k subsets such that the lengths of no
  two subsets differ in length by more than 1"""

  N = len(superset)
  subsets = [[] for i in xrange(k)]

  # main loop to assign every element in superset
  for i in xrange(N):
    # assign 1 element to each subset in turn
    for j in xrange(k):
      if len(superset) == 0:
        break
      rand_index = random.randint(0, len(superset) - 1)
      subsets[j].append(superset[rand_index])
      superset.pop(rand_index)
  return subsets
