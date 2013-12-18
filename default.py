#!/usr/bin/env python

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

import sys
import urllib
import urlparse

from deredactie import parse_feed, START_URL, VIDEO_MIME_TYPE

__addon__ = xbmcaddon.Addon()

self   = sys.argv[0]
handle = int(sys.argv[1])
qs     = sys.argv[2]

if len(qs) > 1:
    params = urlparse.parse_qs(qs[1:])
else:
    params = {}

if 'url' in params:
    url = params['url'][0]
else:
    url = START_URL

(title, entries) = parse_feed(url)
for entry in entries:
    li = xbmcgui.ListItem(entry.title)
    li.setInfo('video', { 'title': entry.title })
    if entry.is_video:
        li.setProperty('mimetype', VIDEO_MIME_TYPE)
        url = entry.url
    else:
        url = self + '?' + urllib.urlencode({ 'url': entry.url })
    xbmcplugin.addDirectoryItem(handle, url, li, not entry.is_video)

xbmcplugin.endOfDirectory(handle, True)
