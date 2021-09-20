from util import *
import json

with open(databasePath, 'r', encoding='utf-8') as jsonFile:
    db = json.load(jsonFile)

exceptions = db['exceptions']['nouns'] 
nouns = db['nouns']
regularNouns = []
for noun in nouns:
    if noun in exceptions:
        print(noun)
    else:
        regularNouns.append(noun)

db['nouns'] = regularNouns
