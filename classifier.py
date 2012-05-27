#!/usr/bin/python

import math

class Classifier(object):
  def __init__(self, fname):
    """Create a new naive Bayesian classifier.
    This classifier trains on a set of data and uses a probability
    density function to classify whether a given example is spam
    or not spam.

    Arguments:
    fname -- the filename (as a string) of the training data"""
    self.training_file = fname
    self.total_samples = 0 # count of the total number of samples used in training
    self.classes = {'spam': 0, 'nonspam': 0} # count of the no. seen samples per class
    self.features = {} # maps the feature name to its Feature object
    self.feat_labels = {} # maps indices to feature names

  def get_classcount(self, cls):
    """Get the number of samples of a specified class."""
    return self.classes[cls]

  def get_featurename(self, index):
    """Get the feature name with the given index."""
    return self.feat_labels[index]

  def get_feature(self, feat_name):
    """Get the Feature object with the specified feature name."""
    return self.features[feat_name]

  def train(self):
    """Train the classifier using the training file given at classifier creation."""
    f_handle = open(self.training_file, 'rU')
    print self.training_file
    # populate the classifier with the feature names
    headers = f_handle.readline().strip().split(',') # read first line & split on the commas
    for i in xrange(len(headers)):
      header = headers[i]
      if header == 'class': # the class is not a feature
        continue
      self.features[header] = Feature(header) # create a new feature
      self.feat_labels[i] = header # associate the feature name with a number for easy lookup
    # populate the values by reading the rest of the lines
    for line in f_handle:
      self.total_samples += 1
      values = line.strip().split(',')
      cls = values[-1] # we are assuming that the class of this row is the last field
      for i in xrange(len(values)):
        value = values[i]
        if value == 'spam' or value == 'nonspam':
          self.classes[value] += 1
          continue
        value = float(value)
        feat_name = self.get_featurename(i)
        self.features[feat_name].add_value(value, cls)

  def classify(self, example):
    """Classify the given example (a comma-separated string) and returns whether
    it is spam or non-spam.

    The argument, example, must be given in the same format as the training data."""
    p_spam = self.get_classcount('spam') / float(self.total_samples)
    p_notsp = self.get_classcount('nonspam') / float(self.total_samples)
    values = example.strip().split(',')
    for i in xrange(len(values)-1): # exclude the last field because that's the class
      value = float(values[i])
      feat_name = self.get_featurename(i)
      feature = self.get_feature(feat_name)
      mean_sp = feature.get_mean('spam')
      mean_notsp = feature.get_mean('nonspam')
      stdev_sp = feature.get_stdev('spam')
      stdev_notsp = feature.get_stdev('nonspam')
      p_spam *= norm_pdf(value, mean_sp, stdev_sp)
      p_notsp *= norm_pdf(value, mean_notsp, stdev_notsp)
    if p_spam > p_notsp:
      return 'spam'
    else: # this includes p_spam <= p_notsp (note less than or equal to)
      # if p_spam < p_notsp, then we'll definitely classify it as spam
      # but if it's p_spam == p_notsp, it could be both so to be safe we classify
      # it as non-spam
      return 'nonspam'

  def get_totalsamplecount(self):
    """Get the total number of samples used to train this classifier."""
    return self.total_samples

  def get_featurenames(self):
    """Get a list of all the feature names in the classifier."""
    return self.feat_labels.values()

  def test_example(self, example):
    """Tests a given example using the classifier.
    Returns True if the classifier was correct, False otherwise.

    The argument example should be of the same format as the training data, ie.
    attr_val1, attr_val2, ... , attr_valn, class
    where attr_val 1 to n are the values of the features, and class is either 'spam'
    or 'nonspam'"""
    expected = example.strip().split(',')[-1] # the last feature is the expected result
    actual = self.classify(example)
    if actual == expected:
      return True
    return False

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
      temp_sum = 0.0
      for value in self.values:
        temp_sum += (value-self.means[cls])**2
      sample_count = float(len(self.values))
      self.stdevs[cls] = math.sqrt(float(temp_sum)/(sample_count-1))
    return self.stdevs[cls]

def norm_pdf(x, mean, stdev):
  """Implements the probability distribution function defined by a given mean
  and standard deviation.
  Used to classify examples with numerical attributes."""
  if stdev == 0:
    return 1
  coefft = 1.0/(stdev*math.sqrt(2*math.pi))
  exponent = -((x-mean)**2)/(2*stdev**2)
  return coefft * math.exp(exponent)
