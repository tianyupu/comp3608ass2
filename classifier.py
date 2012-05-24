#!/usr/bin/python

import math

class Classifier(object):
  def __init__(self, fname):
    self.training_file = fname
    self.total_samples = 0
    self.classes = {'spam': 0, 'nonspam': 0}
    self.features = {}
    self.feat_labels = {}

  def get_classcount(self, cls):
    return self.classes[cls]

  def get_featurename(self, index):
    return self.feat_labels[index]

  def get_feature(self, feat_name):
    return self.features[feat_name]

  def train(self):
    f_handle = open(self.training_file, 'rU')
# populate the headers
    headers = f_handle.readline().strip().split(',')
    for i in xrange(len(headers)):
      header = headers[i]
      if header == 'class':
        continue
      self.features[header] = Feature(header)
      self.feat_labels[i] = header
# populate the values
    for line in f_handle:
      self.total_samples += 1
      values = line.strip().split(',')
      cls = values[-1]
      for i in xrange(len(values)):
        value = values[i]
        if value == 'spam' or value == 'nonspam':
          self.classes[value] += 1
          continue
        value = float(value)
        feat_name = self.get_featurename(i)
        self.features[feat_name].add_value(value, cls)

  def classify(self, example):
    p_spam = self.get_classcount('spam') / float(self.total_samples)
    p_notsp = self.get_classcount('nonspam') / float(self.total_samples)
    values = example.strip().split(',')
    for i in xrange(len(values)):
      value = float(values[i])
      feat_name = self.get_featurename(i)
      feature = self.get_feature(feat_name)
      mean_sp = feature.get_mean('spam')
      mean_notsp = feature.get_mean('nonspam')
      stdev_sp = feature.get_stdev('spam')
      stdev_notsp = feature.get_stdev('nonspam')
      p_spam *= norm_pdf(value, mean_sp, stdev_sp)
      p_notsp *= norm_pdf(value, mean_sp, stdev_sp)
    if p_spam > p_notsp:
      return 'spam'
    else:
      return 'nonspam'

  def get_totalsamplecount(self):
    return self.total_samples

  def get_featurenames(self):
    return self.feat_labels.values()

class Feature(object):
  def __init__(self, name):
    """Create a new Feature object.

    Arguments:
    name -- the name of this feature"""
    self.name = name
    self.values = [] # the feature values for this feature
    self.cls_count = {'spam': 0, 'nonspam': 0} # no. samples for this feature per class
    self.sums = {'spam': 0, 'nonspam': 0} # running total of the values of this feature per class
    self.means = {'spam': 0, 'nonspam': 0}
    self.stdevs = {'spam': 0, 'nonspam': 0}

  def add_value(self, value, cls):
    """Add a new feature value to this feature to the corresponding class."""
    self.values.append(value)
    self.sums[cls] += value # update the running total
    self.cls_count[cls] += 1 # update the sample count

  def get_classcount(self, cls):
    """Get the number of samples for this feature of the specified class."""
    return self.cls_count[cls]

  def get_values(self):
    """Get all the feature values that were observed."""
    return self.values

  def get_featname(self):
    """Get the name of this feature."""
    return self.name

  def get_mean(self, cls):
    """Get the mean for this feature for a particular class.
    Calculates the mean if it hasn't been calculated, else just returns the
    stored value."""
    if self.means[cls] == 0:
      total = self.sums[cls]
      sample_count = float(self.cls_count[cls])
      self.means[cls] = total / sample_count
    return self.means[cls]

  def get_stdev(self, cls):
    """Returns the standard deviation for this feature for a particular class.
    Calculates the standard deviation if it hasn't been calculated, else just
    returns the stored value."""
    if self.stdevs[cls] == 0:
      temp_sum = 0
      for value in self.values:
        temp_sum += (value-self.means[cls])**2
      n = self.cls_count[cls]
      self.stdevs[cls] = 1.0/(n-1) * temp_sum
    return self.stdevs[cls]

def norm_pdf(x, mean, stdev):
  coefft = 1.0/(stdev*math.sqrt(2*math.pi))
  exponent = -((x-mean)**2)/(2*stdev**2)
  return coefft * math.e**exponent
