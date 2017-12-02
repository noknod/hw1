#!/usr/bin/env python


import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8') # required to convert to unicode

print >> sys.stderr, "reporter:counter:Wiki stats,Invalid lines,%d" % 0
print >> sys.stderr, "reporter:counter:Wiki stats,Total words,%d" % 0
print >> sys.stderr, "reporter:counter:Wiki stats,Total lines,%d" % 0

print >> sys.stderr, "============ Debug: mapper started"
for line in sys.stdin:
    print >> sys.stderr, "reporter:counter:Wiki stats,Total lines,%d" % 1
    try:
        article_id, text = unicode(line.strip()).split('\t', 1)
    except ValueError as e:
        print >> sys.stderr, "reporter:counter:Wiki stats,Invalid lines,%d" % 1
        continue
    words = re.split("\W*\s+\W*", text, flags=re.UNICODE)
    for word in words:
        print >> sys.stderr, "reporter:counter:Wiki stats,Total words,%d" % 1
        print "%s\t%d" % (word.lower(), 1)

