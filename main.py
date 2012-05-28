#!/usr/bin/python

if __name__ == '__main__':
  import os.path
  from preprocessor import *
  from classifier import *
  from validation import *

  RESULT_DIR = 'results'

  SUBJ_FNAME = 'subject.csv'
  BODY_FNAME = 'body.csv'

#commented out region creates weighted feature datasets
  directory = sys.argv[1]
  subj_corp, body_corp = preprocess(directory, False)
  stem_subj_corp, stem_body_corp = preprocess(directory, True)
  nfeatures = int(sys.argv[2]) # no. features to select
  subj_sel = feature_select(subj_corp, 'df', nfeatures)
  body_sel = feature_select(body_corp, 'df', nfeatures)
  stem_subj_sel = feature_select(stem_subj_corp, 'df', nfeatures)
  stem_body_sel = feature_select(stem_body_corp, 'df', nfeatures)
  cpd_subj_sel = feature_select(subj_corp, 'cpd', nfeatures)
  cpd_body_sel = feature_select(body_corp, 'cpd', nfeatures)
  cpd_stem_subj_sel = feature_select(stem_subj_corp, 'cpd', nfeatures)
  cpd_stem_body_sel = feature_select(stem_body_corp, 'cpd', nfeatures)
  
  write_dataset(subj_sel, directory, os.path.join(RESULT_DIR, SUBJ_FNAME))
  write_dataset(body_sel, directory, os.path.join(RESULT_DIR, BODY_FNAME))

  write_dataset(stem_subj_sel, directory, os.path.join(RESULT_DIR, "stem_"+SUBJ_FNAME))
  write_dataset(stem_body_sel, directory, os.path.join(RESULT_DIR, "stem_"+BODY_FNAME))

  write_dataset(cpd_subj_sel, directory, os.path.join(RESULT_DIR, "cpd_"+SUBJ_FNAME))
  write_dataset(cpd_body_sel, directory, os.path.join(RESULT_DIR, "cpd_"+BODY_FNAME))

  write_dataset(cpd_stem_subj_sel, directory, os.path.join(RESULT_DIR, "cpd_stem_"+SUBJ_FNAME))
  write_dataset(cpd_stem_body_sel, directory, os.path.join(RESULT_DIR, "cpd_stem_"+BODY_FNAME))

  #cross validation
  cross_validation(SUBJ_FNAME, 10)
  cross_validation(BODY_FNAME, 10)
  cross_validation("stem_"+SUBJ_FNAME, 10)
  cross_validation("stem_"+BODY_FNAME, 10)
  cross_validation("cpd_"+SUBJ_FNAME, 10)
  cross_validation("cpd_"+BODY_FNAME, 10)
  cross_validation("cpd_stem_"+SUBJ_FNAME, 10)
  cross_validation("cpd_stem_"+BODY_FNAME, 10)
