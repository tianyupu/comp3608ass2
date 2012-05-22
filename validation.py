#!/usr/bin/python

import random
import os, os.path

def get_validationsets(folds, source_dir):

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
    

def random_partition(superset, k):
    """Randomly partition superset into k subsets such that the lengths of no
    two subsets differ in length by more than 1"""

    N = len(superset)
    n = N/k

    #assign the k subsets n elements each
    subsets = []
    for i in xrange(k):
        #randomly choose n elements from superset and append to a subset
        subsets.append([])
        rand_indices = random.sample(range(len(superset)), n)
        for rand_index in rand_indices:
            subsets[i].append(superset[rand_index])
        #remove the n elements from superset so they are not chosen again
        for index in sorted(rand_indices, reverse=True):
            superset.pop(index)

    #now randomly assign the remaining elements in the superset to the subsets
    remaining = N - n
    for i in xrange(k):
        #if there are no elements left in the superset, then we are done
        if (len(superset) == 0):
            break
        rand_index = random.randint(0, len(superset) - 1)
        subsets[i].append(superset[rand_index])
        superset.pop(rand_index)

    return subsets
