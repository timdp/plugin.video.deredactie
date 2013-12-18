#!/usr/bin/env python

import re
import time
from urllib2 import urlopen
from xml.dom.minidom import parseString

ATOM_MIME_TYPE = 'application/atom+xml'
THUMBNAIL_MIME_TYPE = 'image/jpeg'
VIDEO_MIME_TYPE = 'video/x-flv'
START_URL = 'http://deredactie.be/cm/vrtnieuws/videozone?mode=atom'

class Item(object):
    def __init__(self, title, date, url):
        self.title = title
        self.date = date
        self.url = url

class VideoItem(Item):
    def __init__(self, title, date, url, thumbnail_url):
        super(VideoItem, self).__init__(title, date, url)
        self.thumbnail_url = thumbnail_url

def parse_feed(url):
    return parse_feed_xml(urlopen(url).read())

def parse_feed_xml(xml):
    dom = parseString(xml)
    title = dom.getElementsByTagName('title')[0].firstChild.data
    entries = []
    for entry_elem in dom.getElementsByTagName('entry'):
        entry = parse_entry(entry_elem)
        entries.append(entry)
    return (title, entries)

def parse_entry(entry_elem):
    title = None
    date = None
    feed_url = None
    video_url = None
    thumbnail_url = None
    for link_elem in entry_elem.getElementsByTagName('link'):
        attr = link_elem.attributes
        rel = attr['rel'].value
        href = attr['href'].value
        mime_type = re.sub(r';.*', '', attr['type'].value)
        if rel == 'enclosure':
            if mime_type == VIDEO_MIME_TYPE:
                video_url = href
            elif mime_type == THUMBNAIL_MIME_TYPE:
                thumbnail_url = href
        elif rel == 'self' and mime_type == ATOM_MIME_TYPE:
            title = attr['title'].value
            feed_url = href
    date_str = entry_elem.getElementsByTagName('published')[0].firstChild.data
    date = time.strptime(date_str[:18], '%Y-%m-%dT%H:%M:%S')
    is_video = (video_url is not None)
    if is_video:
        return VideoItem(title, date, video_url, thumbnail_url)
    else:
        return Item(title, date, feed_url)
