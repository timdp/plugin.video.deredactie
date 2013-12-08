#!/usr/bin/env python

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import sys
import re
import urllib
import urllib2
import cookielib
import HTMLParser
import urlparse

__addon__ = xbmcaddon.Addon()

handle = int(sys.argv[1])
qs = sys.argv[2]

opener = urllib2.build_opener()
opener.addheaders = [
        ('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16'),
    ]
html_parser = HTMLParser.HTMLParser()

def get_url(url):
    resp = opener.open(url)
    content = resp.read()
    charset = resp.headers.getparam('charset')
    if charset is not None:
        content = content.decode(charset)
    resp.close()
    return content

if len(qs) > 1:
    params = urlparse.parse_qs(qs[1:])
    url = params['url'][0]
    title = params['title'][0]

    pat = re.compile('\\bdata-video-iphone-([a-z]+)="([^"]+)"')
    pat2 = re.compile('\\?wowzasessionid=([0-9]+)')

    html = get_url(url)
    for match in pat.finditer(html):
        if match.group(1) == 'server':
            server = match.group(2)
        elif match.group(1) == 'path':
            path = match.group(2)

    base_url = server + '/' + path

    playlist_url = base_url + '/playlist.m3u8';
    m3u = get_url(playlist_url);

    match2 = pat2.match(m3u)
    session_id = match.group(1)

    playlist_url = playlist_url + '?wowzasessionid=' + session_id;
    m3u = get_url(playlist_url)
    for line in m3u.split('\n'):
        if line != '' and line[0] != '#':
            m3u_url = base_url + '/' + line.rstrip()
            break

    li = xbmcgui.ListItem(title)
    li.setInfo('video', { 'title': title })
    li.setProperty('mimetype', 'application/x-mpegURL')
    li.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(handle=handle, url=m3u_url, listitem=li, isFolder=False)

    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

else:
    pat = re.compile('<a href="(/cm/vrtnieuws/videozone/[^"]+_\\d{6}_[^"]+)" class="videolink"[^>]*>(.*?)</a>', re.DOTALL)
    pat2 = re.compile('(?:<span class="title\\b.+?>|<h1>\\s*<span\\b.*>)\\s*(.+?)\\s*(?:</span>|</h1>)', re.DOTALL)
    title_start = '<h3 class="title_before_media">'
    title_end = '</h3>'

    # Get main page HTML
    html = get_url('http://deredactie.be/cm/vrtnieuws/videozone/')
    pos = html.index('<div id="fullwidth"')
    html = html[pos:]
    # Iterate over video links
    for match in pat.finditer(html):
        url = match.group(1)
        html2 = match.group(2)
        match2 = pat2.search(html2)
        # If the title pattern didn't match
        if match2 is None:
            try:
                # Last resort: see if title came before link
                pos1 = html.rindex(title_start, 0, match.span()[0])
                pos2 = html.index(title_end, pos1, match.span()[0])
                title = html[pos1 + len(title_start):pos2]
            except ValueError:
                title = url[url.rindex('/') + 1:]
        else:
            title = match2.group(1)
        title = html_parser.unescape(title)
        url = 'http://deredactie.be' + url

        li = xbmcgui.ListItem(title)
        li.setInfo(type='Video', infoLabels={ 'Title': title })
        item_url = sys.argv[0] + '?' + urllib.urlencode({ 'url': url, 'title': title.encode('utf-8') })
        xbmcplugin.addDirectoryItem(handle=handle, url=item_url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)
