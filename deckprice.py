#!/usr/bin/python3

import os, re, requests, sys

card_quanities = []
card_names = []
card_ids = []
card_prices = []
cards = []

url_api = 'http://api.tcgplayer.com/v1.20.0/'
bearer = 't3qDa3V4oCvGrNgmU04cYYScVbgKOSUwfJB895x3YrcZGqWGUU1iucLRvNIs5BG6gOle5da282RX1zZ5GD1aB6mf6axaaQncWFe0Mc-3EMBRS7FqCa7YelwzKgcNqBtl2pgDlx22rSMG1nut9uTCzHmf2NmI5hxhUGlGKYsAhnjX8axRBXQ0u7q1LnXcc4D_JEF3FBrEROkcKqTGIXABrT3sv5k6OLBSQR1WUHnQj_77_Uqt6JfLq5Dziz09gPUNJpLvxgfLX-DRm6_TCVP8mrYwg9d3hISpwzDVaEHjoa3KXWNQlmlbtzrdxcOl1_p5pM0q1w'

if len(sys.argv) == 1:
    print('deckprice.py <file>')
elif not os.path.isfile(sys.argv[1]):
    print('No such file: ''%s''' % sys.argv[1])
else:
    with open(sys.argv[1]) as f:
        for line in f:
            if re.match(r"^\d+.*$",line):
                card = line.split(" ", 2)
                card_names.append(card[2].rstrip())
   
    for i in range(0,len(card_names)):
        r = requests.get('%scatalog/products?categoryId=1&productTypes=Cards&productName=%s' % (url_api, card_names[i]), headers={'Accept': 'application/json', 'Authorization': 'bearer %s' % bearer})
        card_ids.append(r.json().get('results')[0].get('productId'))

    r = requests.get('%spricing/product/%s' % (url_api, ','.join(map(str, card_ids))), headers={'Accept': 'application/json', 'Authorization': 'bearer %s' % bearer})

    for i in range(0,len(card_names)):
        for j in range(0,len(r.json().get('results'))):
            if r.json().get('results')[j].get('productId') == card_ids[i]:
                card_prices.append(r.json().get('results')[j].get('midPrice'))
                break

    for i in range(0,len(card_names)):
        print("%s\t%s\t%s" % (card_names[i], card_ids[i], card_prices[i]))

