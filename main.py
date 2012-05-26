#!/usr/bin/python

if __name__ == '__main__':
  import os.path
  from preprocessor import *
  from classifier import *

  RESULT_DIR = 'results'

  SUBJ_FNAME = 'subject.csv'
  BODY_FNAME = 'body.csv'

  directory = sys.argv[1]
  subj_corp, body_corp = preprocess(directory, False)
  nfeatures = int(sys.argv[2]) # no. features to select
  subj_sel = feature_select(subj_corp, 'df', nfeatures)
  body_sel = feature_select(body_corp, 'df', nfeatures)
  #write_dataset(subj_sel, directory, os.path.join(RESULT_DIR, SUBJ_FNAME))
  #write_dataset(body_sel, directory, os.path.join(BODY_FNAME))

  subj_classifier = Classifier(os.path.join(RESULT_DIR, SUBJ_FNAME))
  body_classifier = Classifier(os.path.join(RESULT_DIR, BODY_FNAME))
  subj_classifier.train()
  body_classifier.train()
