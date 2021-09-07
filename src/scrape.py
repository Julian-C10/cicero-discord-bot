import requests
from bs4 import BeautifulSoup
from util import databasePath
import json

def remove_extra_whitespace(content):
    newContent = ""
    shouldSkip = False
    for c in content:
        if shouldSkip:
            if c not in '\n\t ':
                shouldSkip = False
                newContent += c
            continue
        if c in "\n\t":
            continue
        elif c == ' ':
            newContent += c
            shouldSkip = True
        else:
            newContent += c
    return newContent

def remove_html_info(content):
    newContent = ""
    shouldSkip = False
    for c in content:
        if shouldSkip:
            if c == ">":
                shouldSkip = False
            continue
        if c == "<":
            shouldSkip = True
            continue
        else:
            newContent += c
    return newContent

def truncate(num):
    strNum = str(num)
    index = strNum.find(".")
    if (index == -1):
        return num
    else:
        return int(strNum[:index])

def parse_table_data(soup, className, audioFilenames, latinText, englishText):
    tableFinalText = []
    tableAudioFilenames = []
    tables = soup.find_all("table", class_=className)
    for table in tables:
        aElements = table.find_all("a")
        divElements = table.find_all("div", align="left")
        for element in aElements:
            tableAudioFilenames.append(element['href'].split('/')[-1])
        for element in divElements:
            trimmed = remove_extra_whitespace(str(element).strip())
            finalText = remove_html_info(trimmed)
            if len(finalText) > 0:
                tableFinalText.append(finalText)    
    count = 0
    isLatin = True
    for i in range(0, len(tableFinalText)):
        if isLatin:
            latinText.append(tableFinalText[i])
        else:
            englishText.append(tableFinalText[i])
        count += 1
        if count == 2:
            isLatin = not isLatin
            count = 0
            audioFilenames.append(tableAudioFilenames[truncate(i / 2)])

def int_to_word(num):
    return translations[num-1]

with open(databasePath, 'r', encoding='utf-8') as jsonFile:
    db = json.load(jsonFile)

translations = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", \
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty", \
    "twentyone", "twentytwo", "twentythree", "twentyfour", "twentyfive", "twentysix", "twentyseven", "twentyeight", "twentynine", "thirty", \
    "thirtyone", "thirtytwo", "thirtythree", "thirtyfour", "thirtyfive", "thirtysix", "thirtyseven", "thirtyeight", "thirtynine", "forty"]

source = "http://wheelockslatin.com/"
for i in range(2, 41):
    audioFilenames = []
    latinText = []
    englishText = []

    if i == 8 or i == 16 or i == 18 or i == 32:
        continue

    URL = f"http://www.wheelockslatin.com/chapters/{int_to_word(i)}/index.html"
    page = requests.get(URL)
    
    if page.status_code != 200:
        print(f"URL returned status code of {page.status_code}. Quitting")
        quit()
        
    soup = BeautifulSoup(page.content, "html.parser")
    parse_table_data(soup, "Alt1", audioFilenames, latinText, englishText)
    parse_table_data(soup, "Alt2", audioFilenames, latinText, englishText)
    
    if (len(latinText) > len(englishText)):
        englishText.append(latinText.pop())
    elif len(englishText) > len(latinText):
        latinText.append(englishText.pop())
        
    if len(audioFilenames) != len(englishText) or len(audioFilenames) != len(latinText):
        print("Lists have different lengths. Quitting")
        quit()
    

    newWords = []
    for j in range(0, len(audioFilenames)):
        word = {}
        word['audioFilename'] = audioFilenames[j]
        word['latin'] = latinText[j]
        word['english'] = englishText[j]
        word['source'] = source
        newWords.append(word)
    
    db[f'chapter {i}']['words'] = newWords
    print(i)

with open(databasePath, "w", encoding='utf-8') as json_file:
    json.dump(db, json_file)