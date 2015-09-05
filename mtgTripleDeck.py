#!/usr/bin/env python

# This script pulls in 3 decklists and generates a metadeck from them.

import argparse
parser = argparse.ArgumentParser()

parser.add_argument('decklists',nargs=3)

args = parser.parse_args()

class constructedDeck:
    def fetchCards(self):
        import os, subprocess, re
        for cardTuple in self.mainboard:
            cleanedName = re.sub(',','',re.sub(' ','',cardTuple[1]))
            if not os.path.isfile('cardJSONs/' + cleanedName + '.json'):
                print 'Fetching:',cardTuple[1]
                #subprocess.check_call(['tutor','card --format json' + " '" + cardTuple[1] + "' " + '> cardJSONs/' + cleanedName + '.json'])
                subprocess.check_call(["tutor card -f json '" + cardTuple[1] + "' > cardJSONs/" + cleanedName + '.json'],shell=True)

def importDeck(filename):
    readfile = open(filename,'r')
    sepfile = readfile.read().split('\n')
    readfile.close()
    
    import re
    sepfile[:] = [re.sub('\[.*?\].','',line).strip() for line in sepfile if not line.startswith('/')]
    if sepfile[-1]=='':
        del sepfile[-1]
    
    deck = constructedDeck()
    
    if len([line for line in sepfile if line.startswith('SB:')]) > 0:
        deck.sideboard = [line[3:].strip().split(' ',1) for line in sepfile if line.startswith('SB:')]
        #print 'Sideboard:',deck.sideboard
        deck.mainboard = [line.split(' ',1) for line in sepfile if not line.startswith('SB:') and not line == '']
    else:
        if sepfile.count('') > 1:
            sepfile.remove('')                  # This removes only the first occurence...
        deck.mainboard = [line.split(' ',1) for line in sepfile[:sepfile.index('')]]
        deck.sideboard = [line.split(' ',1) for line in sepfile[sepfile.index('') + 1:]]
    
    deck.mainboard[:] = [[int(line[0]),line[1]] for line in deck.mainboard]
    deck.sideboard[:] = [[int(line[0]),line[1]] for line in deck.sideboard]
    return deck

decks = [importDeck(filename) for filename in args.decklists]

for deck in decks:
    deck.fetchCards()