#!/usr/bin/env python

import time
from urllib2 import urlopen
from xml.dom.minidom import parseString

VIDEO_MIME_TYPE = 'video/x-flv'
START_URL = 'http://deredactie.be/cm/vrtnieuws/videozone?mode=atom'

class Item:
    def __init__(self, title, url, is_video):
        self.title = title
        self.url = url
        self.is_video = is_video

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

def parse_link(link_elem):
    attr = link_elem.attributes
    rel = attr['rel'].value
    if rel == 'self' \
            or (rel == 'enclosure' and attr['type'].value == VIDEO_MIME_TYPE):
        title = attr['title'].value
        url = attr['href'].value
        is_video = (rel == 'enclosure')
        return Item(title, url, is_video)
    else:
        return None

def parse_entry(entry_elem):
    for link_elem in entry_elem.getElementsByTagName('link'):
        info = parse_link(link_elem)
        if info is not None:
            result = info
            if info.is_video:
                break
    date_str = entry_elem.getElementsByTagName('published')[0].firstChild.data
    result.date = time.strptime(date_str[:18], '%Y-%m-%dT%H:%M:%S')
    return result
