#!/usr/bin/python3
# encoding: utf-8

import os
import random
import subprocess
import sys

threshold=2000
rtime=4000

screensavers = ['aajm', 'asciiquarium', 'cacafire', 'cmatrix', 'maze.py', 'ncmatrix', 'rain -d 200', 'snowjob.py', 'weatherspect']

def main_loop():
	ss_active = None
	screensaver = None
	ptime = 0
	
	while 1:
		idle = float(subprocess.check_output('xprintidle').strip())

		if ss_active:
			ptime +=1

		if idle < threshold and ss_active:
			ss_active = None
			os.system("pkill -f '%s'" % screensavers[screensaver]);		
		elif idle >= threshold and ss_active is None:
			ss_active = 1
			screensaver = random.randint(0, len(screensavers)-1)
			p = subprocess.Popen("urxvt -name cscreensaver -title cscreensaver -e %s" % screensavers[screensaver], stdout=subprocess.PIPE, shell=True)
			subprocess.Popen("wmctrl -r cscreensaver -b toggle,fullscreen", stdout=subprocess.PIPE, shell=True)
		elif ss_active and ptime >= rtime:
			os.system("pkill -f '%s'" % screensavers[screensaver]);
			screensaver = random.randint(0, len(screensavers)-1)
			p = subprocess.Popen("urxvt -name cscreensaver -title cscreensaver -e %s" % screensavers[screensaver], stdout=subprocess.PIPE, shell=True)
			subprocess.Popen("wmctrl -r cscreensaver -b toggle,fullscreen", stdout=subprocess.PIPE, shell=True)
			ptime = 0
	
if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n', file=sys.stderr)
        sys.exit(0)
 
