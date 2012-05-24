#!/usr/bin/python

if __name__ == '__main__':
  from preprocessor import *
  from classifier import *

  SUBJ_FNAME = 'subject.csv'
  BODY_FNAME = 'body.csv'

  directory = sys.argv[1]
  subj_corp, body_corp = preprocess(directory)
  nfeatures = int(sys.argv[2]) # no. features to select
  subj_sel = df_select(subj_corp, nfeatures)
  body_sel = df_select(body_corp, nfeatures)
  write_dataset(subj_sel, directory, SUBJ_FNAME)
  write_dataset(body_sel, directory, BODY_FNAME)

  subj_classifier = Classifier(SUBJ_FNAME)
  body_classifier = Classifier(BODY_FNAME)
