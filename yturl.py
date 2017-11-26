from __future__ import unicode_literals
import youtube_dl
import sys

import urllib.request
import urllib.parse
import re

try:
    query_string = urllib.parse.urlencode({"search_query" : sys.argv})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    link = ("http://www.youtube.com/watch?v=" + search_results[0])
    ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
except:
    sys.exit(1)
