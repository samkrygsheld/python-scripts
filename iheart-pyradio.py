#!/usr/bin/env python3
import parse_iheart_json
import time

f = open('stations.csv', 'a')

for i in range(0, 6973):
    try:
        station = parse_iheart_json.station_info (i, True)
        station_url = parse_iheart_json.get_station_url (station, True)
        f.write('"%s %s %s", "%s"' % (station['name'], station['callLetters'], station['markets'][0]['city'] + ", " + station['markets'][0]['stateAbbreviation'] + ", " + station['markets'][0]['country'], station_url))
        time.sleep (1);
    except:
        pass
f.close()
