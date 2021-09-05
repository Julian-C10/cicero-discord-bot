chapter = input("Chapter: ")
if chapter != 'numbers' and  (not chapter.isnumeric() or int(chapter) < 1 or int(chapter) > 40):
    print("Invalid chapter entry. [1-40] or 'numbers'")
    quit()
latin = input("Latin text (4 forms, don't forget macrons!): ")
english = input("English text: ")
source = input("Source (default wheelock book): ")
if (len(source) == 0):
    source = "Wheelock, Frederic M.; LaFleur, Richard A.. Wheelock's Latin, 7th Edition (The Wheelock's Latin Series). Collins Reference. Kindle Edition." 

word = {}
word['latin'] = latin
word['english'] = english
word['source'] = source

databaseFilename = "../database/database.json"

with open(databaseFilename, "r") as json_file:
    db = json.load(json_file)

relevantWords = db[f'chapter {chapter}']['words']
relevantWords.append(word)
db[f'chapter {chapter}']['words'] = relevantWords

with open(databaseFilename, "w") as json_file:
    json.dump(db, json_file)