#!/usr/bin/python

import os, os.path
import gzip
import sys

import preprocessor

def preprocess(source_dir):
  subj_corp = preprocessor.Corpus()
  body_corp = preprocessor.Corpus()

  src_files = os.listdir(source_dir)
  for f in src_files:
    path = os.path.join(source_dir, f)
    with gzip.open(path) as src_f:
      content = src_f.read()
      content_lines = content.split('\n', 1)
      subj, body = content_lines[0], content_lines[1].strip()
      subj_corp.add(subj, f)
      body_corp.add(body, f)

if __name__ == '__main__':
  directory = sys.argv[1]
  if directory:
  	preprocess(directory)
# select
# normalise
# NB and cross-validation
