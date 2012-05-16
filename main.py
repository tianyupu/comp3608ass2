#!/usr/bin/python

import os, os.path
import gzip
import sys

import preprocessor

subj_corp = preprocessor.Corpus()
body_corp = preprocessor.Corpus()

if sys.argv[1]:
	source_dir = sys.argv[1]
else:
	sys.exit(-1) # needs something more elegant than this

src_files = os.listdir(source_dir)
for f in src_files:
	path = os.path.join(source_dir, f)
  with gzip.open(path) as src_f:
    content = src_f.read()
    content_lines = content.split('\n', 1)
    subj, body = content_lines[0], content_lines[1:]
    subj_corp.add(subj, f)
    body_corp.add(body, f)
