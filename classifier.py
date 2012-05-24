#!/usr/bin/python

def Classifier(object):
  def __init__(self, fname):
    self.training_data = open(fname, 'rU').read()
  def train(self):
    pass
  def classify(self, example):
    pass
