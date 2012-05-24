#!/usr/bin/python

class Classifier(object):
  def __init__(self, fname):
    self.training_file = fname
    self.total_samples = 0
    self.classes = {'spam': 0, 'nonspam': 0}
    self.features = {}
    self.feat_labels = {}
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
      if cls == 'spam':
      	isspam = True
      else:
      	isspam = False
      for i in xrange(len(values)):
      	value = values[i]
        if value == 'spam' or value == 'nonspam':
        	self.classes[value] += 1
        	continue
        value = float(value)
        feat_name = self.feat_labels[i]
        self.features[feat_name].add_value(value, cls)
  def classify(self, example):
    pass
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
