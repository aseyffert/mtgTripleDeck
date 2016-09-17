#!/usr/bin/env python
# This script reads a 

# -------- json import example --------
import json

cardFile = open('farseek.json','r')
loadedCard = json.load(cardFile)
print loadedCard['text']
# -------- --------