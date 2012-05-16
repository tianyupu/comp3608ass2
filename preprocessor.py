#!/usr/bin/python

import re

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
    self.words = {}
    _populate_stopw()
  def _populate_stopw(self):
    """A helper method to extract the stop words from the stop words file."""
    f_handle = open(self.STOPFILE, 'rU')
    for word in f_handle.readlines():
    	self.STOPWORDS.add(word)
  def get_stopwords(self):
    """Return the set of stop words used as a Python list."""
    return list(self.STOPWORDS)
  def get_words(self):
    """Get all the words for this corpus."""
    return self.words.keys()
  def get_df(self, word):
    """Get the document frequency (DF) for a particular word.
    
    If the word is not found, return 0."""
    word = word.lower()
    if word in self.words:
    	return len(self.words[word])
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
      	self._add_word(word, fname)
  def _add_word(self, word, fname):
    """A helper method to add a word to the corpus. The word must be a string.
    """
    word = word.lower()
    if word in self.words:
      doc_freqs = self.words[word]
    else:
    	self.words[word] = {}
    if fname in doc_freqs:
    	doc_freqs[fname] += 1
    else:
    	doc_freqs[fname] = 1
