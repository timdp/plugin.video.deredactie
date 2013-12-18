#!/usr/bin/env python

import sys
import time

from deredactie import parse_feed, START_URL

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = START_URL

(title, entries) = parse_feed(url)

print 'Title: {0}'.format(title)

for entry in entries:
    date = time.strftime('%Y-%m-%d %H:%M:%S', entry.date)
    print '\n- {0}\n  Date: {1}\n  Video: {2}\n  URL: {3}'.format(
        entry.title.encode('utf-8', 'ignore'), date, entry.is_video, entry.url)
