#!/usr/bin/python

if __name__ == '__main__':
  from preprocessor import *
  directory = sys.argv[1]
  subj_corp, body_corp = preprocess(directory)
  nfeatures = int(sys.argv[2])
  subj_sel = df_select(subj_corp, nfeatures)
  body_sel = df_select(body_corp, nfeatures)
  write_dataset(subj_sel, directory, 'subject.csv')
  write_dataset(body_sel, directory, 'body.csv')
# NB and cross-validation
