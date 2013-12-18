#!/usr/bin/env python

import sys
import time

from deredactie import VideoItem, parse_feed, START_URL

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = START_URL

(title, entries) = parse_feed(url)

print 'Title: {0}'.format(title)

for entry in entries:
    print '\n- {0}\n  Date:  {1}\n  URL:   {2}'.format(
        entry.title.encode('utf-8', 'ignore'),
        time.strftime('%Y-%m-%d %H:%M:%S', entry.date),
        entry.url
    )
    if isinstance(entry, VideoItem):
        print '  Thumb: {0}'.format(entry.thumbnail_url)
