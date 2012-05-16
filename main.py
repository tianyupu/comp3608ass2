#!/usr/bin/python

import os, os.path
import gzip
import sys
import Corpus

subj_corp = Corpus()
body_corp = Corpus()

if sys.argv[1]:
	source_dir = sys.argv[1]

src_files = os.listdir(source_dir)
for f in src_files:
	path = os.path.join(source_dir, f)
  with gzip.open(path) as src_file:
    content = src_file.read()
    content_lines = content.splitlines()
    subj, body = content_lines[0], content_lines[1:]
    subj_corp.add(subj)
    body_corp.add(body)
