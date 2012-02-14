# -*- coding: utf-8 -*-
"""Tools to deal with text processing."""
import re
import string
from nltk.tokenize import WhitespaceTokenizer
from synt import config

#ordinal -> none character mapping
PUNC_MAP = dict([(ord(x),None) for x in string.punctuation])

FORMAT_PATS = (
        # remove re-tweets
        (re.compile("@[A-Za-z0-9_]+"), ''),

        # remove hash tags
        (re.compile("#"), ''),

        # remove occurences of more than two consecutive repeating characters
        (re.compile("(\w)\\1{2,}"), "\\1\\1"),

        # remove html tags
        (re.compile("<[^<]+?>"), ''),

        # get rid of any left over urls
        (re.compile("(http|www)[^ ]*"), ''),
    )

def normalize_text(text):
    """
    Formats text to strip unneccesary:words, punctuation and whitespace. Returns a tokenized list.

    Arguments:
    text (str) -- Text to process.

    >>> text = "ommmmmmg how'r u!? visi t  <html> <a href='http://google.com'> my</a> site @ http://www.coolstuff.com haha"
    >>> normalize_text(text)
    [u'ommg', u'howr', u'visi', u'my', u'site', u'haha']

    >>> normalize_text("FOE JAPAN が粘り強く主張していた避難の権利")
    [u'foe', u'japan', u'\u304c\u7c98\u308a\u5f37\u304f\u4e3b\u5f35\u3057\u3066\u3044\u305f\u907f\u96e3\u306e\u6a29\u5229']

    >>> normalize_text('no ')
    [u'no']

    >>> normalize_text('')
    >>>
    """

    if not text: return

    if not isinstance(text, unicode):
        #make sure we're using unicode
        text = unicode(text, 'utf-8')

    text = text.lower()

    for pat, subl in FORMAT_PATS:
        text = pat.sub(subl, text)

    _tmp = set()
    for e in config.EMOTICONS:
        if e in text:
            _tmp.add(e)

    text = text.translate(PUNC_MAP).strip() + ' ' #remove punctuation
    if _tmp:
        text += ' '.join([e for e in _tmp]) #attach emoticons back

    if text:
        #tokenize on words longer than 1 char
        words = [w for w in WhitespaceTokenizer().tokenize(text) if len(w) > 1]

        return words

if __name__ == '__main__':
    import doctest
    doctest.testmod()
