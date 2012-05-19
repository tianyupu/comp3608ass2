#!/usr/bin/python

import re
import os, os.path, sys
import gzip
from math import log10, sqrt

class Corpus(object):
  """A class to represent a corpus of text.

  Initialised with no parameters.

  Class constants:
  WORD_PATT - determines what sort of terms the corpus retains
  STOPFILE - the filename of the file containing the stop words
  STOPWORDS - the set of stop words extracted from the file
  """
  WORD_PATT = re.compile(r'([A-Za-z])+', re.IGNORECASE)
  STOPFILE = 'english.stop'
  STOPWORDS = set()

  def __init__(self):
    """Create a new, empty corpus of text."""
    self.doc_count = 0
    self.words = WordList()
    self._populate_stopw()
  def _populate_stopw(self):
    """A helper method to extract the stop words from the stop words file."""
    f_handle = open(self.STOPFILE, 'rU')
    for word in f_handle.read().splitlines():
      self.STOPWORDS.add(word)
  def get_stopwords(self):
    """Return the set of stop words used as a Python list."""
    return list(self.STOPWORDS)
  def get_words(self):
    """Get all the words for this corpus."""
    return self.words.get_words()
  def get_word(self, word):
    """Return the word object corresponding to the specified word."""
    return self.words.get_word(word)
  def get_df(self, word):
    """Get the document frequency (DF) for a particular word.
    
    If the word is not found, return 0."""
    word_obj = self.words.get_word(word)
    if word_obj:
      return word_obj.get_df()
    else:
      return 0
  def add(self, text, fname):
    """Add a string of text to the corpus by first splitting it into features
    defined by WORD_PAT, and then removing stop words.

    Takes a string as its argument."""
    for match in re.finditer(self.WORD_PATT, text):
      if match:
        word = match.group(0)
        if word in self.STOPWORDS:
          continue
        self.words.add_word(word, fname)

class Word(object):
  def __init__(self, word, fname):
    """Create a new word object, for use in the Corpus.

    Arguments:
    word -- the actual word that this object holds
    fname -- the name of the file that this word first appeared in
    """
    self.freqs = {}
    self.word = word
    self.freqs[fname] = 1
  def update_freq(self, fname):
    """Update the value of the frequencies of this word.

    If the word has already been in the file, increment the counter.
    If not, add a new entry to indicate that is word has been seen in the file
    called fname."""
    if fname in self.freqs:
      self.freqs[fname] += 1
    else:
      self.freqs[fname] = 1
  def get_df(self):
    """Get the number of documents in the corpus that the word appears in."""
    return len(self.freqs)
  def get_freq(self, fname):
    """Get the number of occurences of this word in a particular file."""
    if fname in self.freqs:
      return self.freqs[fname]
    else:
      return 0
  def get_text(self):
    """Get the actual word that this object holds, as a string."""
    return self.word
  def get_filenames(self):
    """Returns a list of the filenames that this word appears in."""
    return self.freqs.keys()
  def __repr__(self):
    return self.word
  def __str__(self):
    return self.word
  def __eq__(self, other):
    if self.word == other.get_text():
      return True
    return False
  def __ne__(self, other):
    if self.word != other.get_text():
      return True
    return False

class WordList(object):
  def __init__(self):
    self.words = {}
  def add_word(self, word, fname):
    if word in self.words:
      word_obj = self.words[word]
      word_obj.update_freq(fname)
    else:
      word_obj = Word(word, fname)
      self.words[word] = word_obj
  def get_words(self):
    return self.words.values()
  def get_word(self, text):
    if text in self.words:
      return self.words[text]
    return None

def preprocess(source_dir):
  subj_corp = Corpus()
  body_corp = Corpus()

  src_files = os.listdir(source_dir)
  for f in src_files:
    path = os.path.join(source_dir, f)
    src_f = gzip.open(path)
    #with gzip.open(path) as src_f:
    content = src_f.read()
    content_lines = content.split('\n', 1)
    subj, body = content_lines[0].strip(), content_lines[1].strip()
    subj = subj.lstrip('Subject: ')
    subj_corp.add(subj, f)
    body_corp.add(body, f)
    src_f.close()
  return subj_corp, body_corp

def df_select(corpus, max_no):
  df_vals = {}
  selected = []
  count = 0
  for word in corpus.get_words():
    df = word.get_df()
    if df in df_vals:
      df_vals[df].append(word)
    else:
      df_vals[df] = [word]
  for df_val in sorted(df_vals, reverse=True):
    while df_vals[df_val]:
      if count < max_no:
        word = df_vals[df_val].pop()
        selected.append(word)
        count += 1
      else:
        return sorted(selected)
#    df_vals.append((corpus.get_df(word), corpus.get_word(word)))
#  df_vals.sort(cmp=lambda x,y:cmp(x[0],y[0]), reverse=True)
#  return df_vals[:max_no]

def write_dataset(df_list, src_dir, sav_name):
  nfeatures = len(df_list)
  header_list = ['f%d' % x for x in xrange(1,nfeatures+1)]
  header_list.append('class')
  header_str = ','.join(header_list) + '\n'

  src_files = sorted(os.listdir(src_dir))
  collection_size = len(src_files)
  weights = []
  for f in src_files:
    row = []
    for word_obj in df_list:
      row.append(str(cos_norm(word_obj, f, df_list, collection_size)))
    if 'spmsg' in f:
      row.append('spam')
    else:
      row.append('nonspam')
    row_str = ','.join(row)
    weights.append(row_str)
  weight_str = '\n'.join(weights)

  out_f = open(sav_name, 'w')
  out_f.write(header_str+weight_str)
  out_f.close()

def tf_idf(word, fname, collection_size):
  # tfidf(t_k, d_j) = #(t_k, d_j) * log(|Tr| / #Tr(t_k))
  tf_idf = word.get_freq(fname) * log10(float(collection_size)/word.get_df())
  return tf_idf

def cos_norm(word, fname, words, collection_size):
  numerator = tf_idf(word, fname, collection_size)
  denom = 0.0
  for word in words:
    denom += tf_idf(word, fname, collection_size) ** 2
  if denom == 0:
    weight = 0
  else:
    weight = numerator / sqrt(denom)
  return weight
