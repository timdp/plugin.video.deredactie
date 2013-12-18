#!/usr/bin/env python

import sys

from deredactie import parse_feed

url = sys.argv[1]
(title, entries) = parse_feed(url)
print 'Title: {0}'.format(title)
for entry in entries:
    print '\n- {0}\n  Video: {1}\n  {2}'.format(
        entry.title, entry.is_video, entry.url)
