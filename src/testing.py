import json

fileName = "tempVocabAdd.txt"

with open(fileName, "r", encoding='utf8') as file:
    text = file.read()

text = sorted(text.split('\n'), key=str.lower)
text = "\n".join(text)

with open(fileName, "w", encoding='utf8') as file:
    file.write(text)