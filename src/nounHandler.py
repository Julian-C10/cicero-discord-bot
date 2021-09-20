from util import *
import json
import os.path
import discord

cases = ["Nominative", "Genitive", "Dative", "Accusative", "Ablative", "Vocative"]
firstDeclSinEndings = ["a", "ae", "ae", "am", "ā", "a"]
firstDeclPluEndings = ["ae", "ārum", "is", "ās", "īs", "ae"]
secondDeclSinEndingsEr = ["er", "ī", "ō", "um", "ō", "er"]
secondDeclSinEndingsUs = ["us", "ī", "ō", "um", "ō", "e"]
secondDeclSinEndingsEr = ["er", "ī", "ō", "um", "ō", "er"]
secondDeclPluEndings = ["ī", "ōrum", "īs", "ō", "īs", "ī"]

notSuppDecl = ["3rd Declension", "4th Declension", "5th Declension"]

def get_proper_forms(noun, decl, number):
    base = noun['base']
    nomSin = noun['latin'].split(',')[0]
    forms = []
    endings = []
    isErNoun = False

    if decl == "1st Declension" and number == "Singular":
        endings = firstDeclSinEndings
    elif decl == "1st Declension" and number == "Plural":
        endings = firstDeclPluEndings
    elif decl == "2nd Declension" and nomSin.endswith("er") and number == "Singular":
        isErNoun = True
        endings = secondDeclSinEndingsEr
    elif decl == "2nd Declension" and nomSin.endswith("us") and number == "Singular":
        endings = secondDeclSinEndingsUs
    elif decl == "2nd Declension" and number == "Plural":
        endings = secondDeclPluEndings

    assert len(endings) > 0

    for i in range(0, len(endings)):
        if isErNoun and (i == 0  or i == len(endings) - 1):
            forms.append(f'{base[:-1]}{endings[i]}')
        else:
            forms.append(f'{base}{endings[i]}')

    return forms
    
def get_col2(noun, number):
    decl = noun['declension']
    col2 = []
    if decl in notSuppDecl:
        col2.append("error")
        return col2
    col2.append(noun['gender'])
    forms = get_proper_forms(noun, noun['declension'], number)
    for form in forms:
        col2.append(form)
    return col2
    

def longest_line_length(col):
    maxLen = len(col[0])
    for i in range(1, len(col)):
        if len(col[i]) > maxLen:
            maxLen = len(col[i])
    return maxLen

def get_col1(base):
    col1 = []
    col1.append(base)
    for case in cases:
        col1.append(case)
    return col1

def create_border_row(col1Max, col2Max):
    row = ""
    for i in range (0, col1Max + 1):
        row += '-'
    row += '|'
    for i in range (0, col2Max + 2):
        row += '-'
    row += '|'
    return row

def create_row(col1Form, col2Form, col1Max, col2Max):
    row = " "
    for i in range (0, col1Max): 
        if i < len(col1Form):
            row += col1Form[i]
        else:
            row += " "
    row += '| '
    for i in range (0, col2Max): 
        if i < len(col2Form):
            row += col2Form[i]
        else:
            row += " "
    row += ' |'
    return row
    
def get_table_str(noun, number):
    tableStr = f'{number}\n'
    base = noun['base']
    col1 = get_col1(f'{base}-')
    col1MaxLine = longest_line_length(col1)
    col2 = get_col2(noun, number)
    if col2[0] == "error":
        return "error"
    assert len(col1) == len(col2)
    col2MaxLine = longest_line_length(col2)
    borderRow = create_border_row(col1MaxLine, col2MaxLine)
    tableStr += borderRow + '\n'
    for i in range(0, len(col1)):
        tableStr += create_row(col1[i], col2[i], col1MaxLine, col2MaxLine) + '\n'
        tableStr += borderRow + '\n'
    return tableStr
        
def decline_noun(noun):
    sinDeclined = get_table_str(noun, 'Singular')
    if (sinDeclined == "error"):
        return "error"
    fileStr = sinDeclined
    fileStr += '\n\n'
    pluDeclined = get_table_str(noun, 'Plural')
    if pluDeclined == "error":
        return "error"
    fileStr += pluDeclined
    return fileStr

async def send_declined_word(message, splitMsg, db):
    desiredWords = splitMsg[1:]
    index = -1
    nouns = db['nouns']
    for num in range(0, len(nouns)):
        found = True
        for desiredWord in desiredWords:
            latinText = nouns[num]['latin'].lower()
            englishText = nouns[num]['english'].lower()
            if desiredWord not in latinText and desiredWord not in englishText:
                found = False
                break
        if found:
            index = num
            break
                
    if index == -1:
        reconstructedMsg = ' '.join(desiredWords)
        await message.channel.send(missing_noun_error(reconstructedMsg))
    
    else:
        noun = nouns[index]
        transcript = f"{noun['latin']}\n*{noun['english']}*\n{noun['declension']}\n"
        dirPath = construct_decline_dir_path()
        if not os.path.isdir(dirPath):
            os.mkdir(dirPath)
        filePath = construct_decline_path(noun['latin'])
        if not(os.path.isfile(filePath)):
            table = decline_noun(noun)
            if (table == "error"):
                reconstructedMsg = ' '.join(desiredWords)
                await message.channel.send(unable_to_decline_noun_error(reconstructedMsg))
                return
            with open(filePath, 'w', encoding='utf8') as nounDeclination:
                nounDeclination.write(table)
        fileName = filePath.split("/")[-1]
        await message.channel.send(file=discord.File(fp=filePath, filename=fileName), content=transcript)

async def send_all_nouns_list(message, splitMsg, db):
    filePath = construct_noun_list_path("")
    dirPath = construct_noun_list_dir_path()
    if not(os.path.isfile(filePath)):
        nouns = db['nouns']
        longestLineLen = longest_line_length_util(nouns, 'latin')
        msg = ''
        for noun in nouns:
            msg += list_string_format(longestLineLen + 5, noun['latin'], noun['english'])
        msgList = msg.split("\n")
        msgList = sorted(msgList, key=str.casefold)
        msg = "\n".join(msgList)
        if not os.path.isdir(dirPath):
            os.mkdir(dirPath)
        with open(filePath, 'w', encoding='utf8') as nounList:
            nounList.write(msg)
    await message.channel.send(file=discord.File(fp=filePath))

def format_declension(decl):
    formattedDecl = ""
    if decl == "1st" or decl == "1":
        formattedDecl = "1st Declension"
    elif decl == "2nd" or decl == "2":
        formattedDecl = "2nd Declension"
    elif decl == "3rd" or decl == "3":
        formattedDecl = "3rd Declension"
    elif decl == "4th" or decl == "4":
        formattedDecl = "4th Declension"
    elif decl == "5th" or decl == "5":
        formattedDecl = "5th Declension"

    assert len(formattedDecl) > 0

    return formattedDecl
    
async def send_noun_list(message, splitMsg, db):
    if len(splitMsg) == 2:
        await send_all_nouns_list(message, splitMsg, db)
        return
    if len(splitMsg) != 3 and len(splitMsg) != 4:
        await message.channel.send(standard_error_message)
        return

    decl = splitMsg[2]
    if decl not in ["1st", "2nd", "3rd", "4th", "5th", "1", "2", "3", "4", "5"]:
        await message.channel.send(standard_error_message)
        return
    decl = format_declension(decl)
    filePath = construct_noun_list_path(decl)
    dirPath = construct_noun_list_dir_path()
    if not(os.path.isfile(filePath)):
        nouns = db['nouns']
        longestLineLen = longest_line_length_util(nouns, 'latin')
        msg = ''
        for noun in nouns:
            if noun['declension'] == decl:
                msg += list_string_format(longestLineLen + 5, noun['latin'], noun['english'])
        msgList = msg.split("\n")
        msgList = sorted(msgList, key=str.casefold)
        msg = "\n".join(msgList)
        if not os.path.isdir(dirPath):
            os.mkdir(dirPath)
        with open(filePath, 'w', encoding='utf8') as nounList:
            nounList.write(msg)
    await message.channel.send(file=discord.File(fp=filePath))
