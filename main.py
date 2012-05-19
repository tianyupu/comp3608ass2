#!/usr/bin/python

if __name__ == '__main__':
  from preprocessor import *
  directory = sys.argv[1]
  if directory:
  	subj_corp, body_corp = preprocess(directory)
  else:
    sys.stderr.write('main.py: no directory specified, exiting\n')
# select
# normalise
# NB and cross-validation
