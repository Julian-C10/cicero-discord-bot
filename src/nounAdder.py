from util import *
import json

def get_base(decl, genSin):
    base = ""
    if (decl == "2nd Declension"):
        base = genSin[:-1]
    else:
        base = genSin[:-2]
    return base

def has_one_gender(latinText):
    i = 0
    if ("(f)" in latinText):
        i += 1
    if ("(m)" in latinText):
        i += 1
    if ("(n)" in latinText):
        i += 1
    return i == 1

def get_gender(noun):
    parenthesesGender = noun['latin'].split(' ')[-1]
    gender = ""
    if parenthesesGender == "(f)":
        gender = "Female"
    elif parenthesesGender == "(m)":
        gender = "Male"
    elif parenthesesGender == "(n)":
        gender = "Neuter"

    if len(gender) <= 0:
        print(noun)
    assert len(gender) > 0
    return gender

def get_declension(genSin):
    decl = ""
    if genSin.endswith("ae"):
        decl = "1st Declension"
    elif genSin.endswith("ēī"):
        decl = "5th Declension"
    elif genSin.endswith("ūs"):
        decl = "4th Declension"
    elif genSin.endswith("is"):
        decl = "3rd Declension"
    elif genSin.endswith("ī"):
        decl = "2nd Declension"

    return decl

with open(databasePath, 'r', encoding='utf-8') as jsonFile:
    db = json.load(jsonFile)

nouns = []
filteredNouns = []
exceptions = []

preps = ["to ", "at ", "from ", "by ", "with "]

for i in range(1, 41):
    words = db[f'chapter {i}']['words']
    for j in range(0, len(words)):
        latinText = words[j]['latin']
        englishText = words[j]['english'] 
        if (latinText.endswith("(f)") or latinText.endswith("(m)") or
        latinText.endswith("(n)")):
            item = {}
            item['latin'] = words[j]['latin']
            item['english'] = words[j]['english']
            item['source'] = words[j]['source']
            nouns.append(item)

for noun in nouns:
    if len(noun['latin'].split(',')) >= 2 and has_one_gender(noun['latin']):
        filteredNouns.append(noun)

for noun in filteredNouns:
    genSin = noun['latin'].split(' ')[1]
    
    decl = get_declension(genSin)
    noun['gender'] = get_gender(noun)
    if len(decl) == 0:
        exceptions.append(noun)
        continue
    assert len(decl) > 0
    noun['declension'] = decl
    noun['base'] = get_base(noun['declension'], genSin)

db['nouns'] = filteredNouns
db['exceptions'] = {}
db['exceptions']['nouns'] = exceptions

with open(databasePath, "w") as json_file:
    json.dump(db, json_file)