#!/usr/bin/python

import gzip
import os, os.path
import sys

class Corpus(object):
  def __init__(self, directory):
    self.directory = directory
    # initialise subject and body subcorpuses
  def _extract_words(self):
    msgs = os.listdir(self.directory)
    for msg in msgs:
    	path = os.path.join(self.directory, msg)
      with gzip.open(path) as msgfile:
        content = msgfile.read()
        content_lines = content.splitlines()
        subject, body = content_lines[0], content_lines[1:]
# remove stop words
# create the respective corpora
  def _remove_stopw(self):
    pass
  def get_stopfname(self):
    return
  def get_subjectcorp(self):
    return
  def get_bodycorp(self):
    return
