from util import *
import json

with open(databasePath, 'r', encoding='utf-8') as jsonFile:
    db = json.load(jsonFile)

for noun in db['nouns']:
    print(noun)