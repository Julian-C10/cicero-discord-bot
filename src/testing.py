import json

databaseFilename = "../database/database.json"

with open(databaseFilename, "r") as json_file:
    db = json.load(json_file)

with open(databaseFilename, "w") as json_file:
    json.dump(db, json_file)