import json

chapter = input("Chapter: ")
if not chapter.isnumeric() or int(chapter) < 1 or int(chapter) > 40:
    print("Invalid chapter entry. [1-40] or 'numbers'")
    quit()
latin = input("Latin text (4 forms, don't forget macrons!): ")
if len(latin) == 0:
    print("Invalid latin text entry, needs to contain text.")
    quit()
english = input("English text: ")
if len(english) == 0:
    print("Invalid english text entry, needs to contain text.")
    quit()
source = input("Source (default wheelock book): ")
if (len(source) == 0):
    source = "Wheelock, Frederic M.; LaFleur, Richard A.. Wheelock's Latin, 7th Edition (The Wheelock's Latin Series). Collins Reference. Kindle Edition." 

word = {}
word['latin'] = latin
word['english'] = english
word['source'] = source

databaseFilename = "../database/database.json"

with open(databaseFilename, "r", encoding='utf8') as json_file:
    db = json.load(json_file)

relevantWords = db[f'chapter {chapter}']['words']
relevantWords.append(word)
db[f'chapter {chapter}']['words'] = relevantWords

with open(databaseFilename, "w") as json_file:
    json.dump(db, json_file)