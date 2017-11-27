#!/usr/bin/python
# -*- coding: utf-8 -*-

# Put your newsbeuter cache messages in Maildir directories

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Newsbeuter stores its feeds in ~/.newsbeuter/cache.db. This file is a
# SQLite3 database with 2 tables. The table named rss_item contains all
# of the RSS/Atom messages. The "body" of the message is stored in HTML
# (without the headers).

# This Python script converts the messages of your cache.db file to
# Maildir repositories. The RSS/Atom messages are put in their
# respective Maildir...

# modules import
from email.mime.text import MIMEText
import email.utils
import mailbox
import sqlite3
import sys

# Dictionary for feedurl to Maildir directories association:
# You have to manually change thoses references for your feeds
# Keys are feedurl from newsbeuter, items are the name of the sub-maildir
feed2mail = { 'http://www.maitre-eolas.fr/feed/atom':'Feeds.Eolas',
              'https://medspx.homelinux.org/blog/index.rss20':'Feeds.WhereIsIt',
              'http://planet.debian.net/rss20.xml':'Feeds.planetDebian',
              'http://feeds2.feedburner.com/hackaday/LgoM':'Feeds.HackADay',
              'https://www.adafruit.com/blog/feed/':'Feeds.Adafruit',
              'https://linuxfr.org/news.atom':'Feeds.LinuxFr',
              'http://www.bortzmeyer.org/feed-full.atom':'Feeds.Bortzmeyer',
              'http://www.la-grange.net/feed.atom':'Feeds.LaGrange'}

# Part 1: Arguments analysis
if len(sys.argv) < 2:
    print 'newsbeuter2maildir.py cache.db_file maildir'
    exit(1)

cache_file = sys.argv[1]
maildir = sys.argv[2]

print 'extracting from %s to %s ...' % (cache_file, maildir)

# Part 2: extract messages from cache.db
cache = sqlite3.connect(cache_file)
destination = mailbox.Maildir(maildir)

c = cache.cursor()
# We only want to extract the items that have been read and which are
# not deleted
c.execute('select title, author, feedurl, pubDate, content from'
         + ' rss_item where unread=0 and deleted=0')
# for every line, we put a message in the right mailbox
for line in c:
    header = u'<html><head></head><body>'.encode('utf-8')
    footer = u'</body></html>'.encode('utf-8')
    msg = MIMEText(header+line[4].encode('utf-8')+footer, 'html')
    msg['Subject'] = line[0].encode('utf-8')
    msg['From'] = line[1].encode('utf-8')
    msg['Date'] = email.utils.formatdate(float(line[3]))
    if line[2] in feed2mail.keys():
      feed = feed2mail[line[2]]
        # If the maildir doesn't exist, we create it.
        if feed not in destination.list_folders():
            print "maildir", feed, "doesn't exist: we create it !"
            maildir_feed = destination.add_folder(feed)
        else:
              maildir_feed = destination.get_folder(feed)
        # Add the message to the maildir and mark it unread:
        msg_in_feed = mailbox.MaildirMessage(msg)
        msg_in_feed.set_flags('S')
        msg_key = maildir_feed.add(msg_in_feed)
    else: 
        print "Unknown Feed:",line[2]

destination.close()

exit(0)
  