import os
import json

databaseFilename = 'database\database.json'

with open(databaseFilename, "r") as json_file:
    db = json.load(json_file)

item = {}
item["audioFilename"] = ""
item["transcript"] = ""
item["source"] = ""

new_thing = {}
new_thing["audioFiles"] = {}

for i in range(1, 41):
    addedItems = []
    item = {}
    currCh = "chapter " + str(i)
    filepath = "sounds/" + str(i) + "/vocabulary"
    currDir = os.listdir(filepath)
    for filename in currDir:
        if filename.endswith(".mp3"):
            item["audioFilename"] = filename
            item["source"] = "http://wheelockslatin.com/"
            addedItems.append(item)
            item = {}
    db[currCh] = {}
    db[currCh]["audioFiles"] = addedItems

with open(databaseFilename, "w") as json_file:
    json.dump(db, json_file)