import discord
import random
import os.path
from util import standard_error_message

# List all vocab words in the chapter
async def send_vocab_extended_list(message, splitMsg, db):
    filePath = construct_vocab_extended_list_path(splitMsg[1])
    if not(os.path.isfile(filePath)):
        num = splitMsg[1]
        words = db[f'chapter {splitMsg[1]}']['words']
        if 'latin' not in words[0].keys():
            await message.channel.send(standard_error_message)
            return
        longestLineLen = longest_line_length(words, 'latin', isExtended=True)
        msg = ''
        for i in range(0, len(words)):
            msg += list_string_format(longestLineLen + 5, words[i]['latin'], words[i]['english'])
        with open(filePath, 'w', encoding='utf8') as vocabList:
            vocabList.write(msg)
    await message.channel.send(file=discord.File(fp=filePath))

async def send_vocab_list(message, splitMsg, db):
    filePath = construct_vocab_list_path(splitMsg[1])
    if not(os.path.isfile(filePath)):
        num = splitMsg[1]
        words = db[f'chapter {splitMsg[1]}']['words']
        if 'latin' not in words[0].keys():
            await message.channel.send(standard_error_message)
            return
        longestLineLen = longest_line_length(words, 'latin', isExtended=False)
        msg = ''
        for i in range(0, len(words)):
            if 'audioFilename' in words[i].keys():
                msg += list_string_format(longestLineLen + 5, words[i]['latin'], words[i]['english'])
        with open(filePath, 'w', encoding='utf8') as vocabList:
            vocabList.write(msg)
    await message.channel.send(file=discord.File(fp=filePath))

# List all vocab words in chapter in one language
async def send_vocab_test(message, splitMsg, db):
    desiredLang = splitMsg[4]
    filePath = construct_vocab_test_path(splitMsg[1], desiredLang)
    if not(os.path.isfile(filePath)):
        num = splitMsg[1]
        words = db[f'chapter {splitMsg[1]}']['words']
        if 'latin' not in words[0].keys():
            await message.channel.send(standard_error_message)
            return
        longestLineLen = longest_line_length(words, desiredLang, isExtended=False)
        msg = ''
        for i in range(0, len(words)):
            if 'audioFilename' in words[i].keys():
                msg += test_string_format(longestLineLen + 1, words[i][desiredLang])
        with open(filePath, 'w', encoding='utf8') as vocabList:
            vocabList.write(msg)
    await message.channel.send(file=discord.File(fp=filePath))
    
# Display a random vocab word in the chapter
async def send_random_word(message, splitMsg, db):
    num = splitMsg[1]
    words = db['chapter ' + num]['words']
    if 'latin' not in words[0].keys():
        await message.channel.send(standard_error_message)
        return
    index = random.randint(0, len(words) - 1)
    word = words[index]
    transcript = f"{word['latin']}\n*{word['english']}*"
    if 'audioFilename' in word.keys():
        filepath = construct_sound_path(num, word['audioFilename'])
        await message.channel.send(file=discord.File(fp=filepath, filename="audio.mp3"), content=transcript)
    else:
        await message.channel.send(transcript)

# Display a specific vocab word in the chapter
async def send_specific_word(message, splitMsg, db):
    num = splitMsg[1]
    desiredWord = splitMsg[4]
    words = db['chapter ' + num]['words']
    if 'latin' not in words[0].keys():
        await message.channel.send(standard_error_message)
        return
    index = -1
    for i in range(0, len(words)):
        if desiredWord in words[i]['latin'] or desiredWord in words[i]['english']:
            index = i
            break
    if index == -1:
        await message.channel.send(f'Sorry, I couldn\'t find a vocab entry for "{desiredWord}" in chapter {num}.')
    else:
        word = words[index]
        transcript = f"{word['latin']}\n*{word['english']}*"
        if 'audioFilename' in word.keys():
            filepath = construct_sound_path(num, word['audioFilename'])
            await message.channel.send(file=discord.File(fp=filepath, filename="audio.mp3"), content=transcript)
        else:
            await message.channel.send(transcript)


def construct_sound_path(num, filename):
    return f'../sounds/{num}/vocabulary/{filename}'

def construct_vocab_list_path(num):
    return f'../vocab-lists/{num}/ch{num}-vocab-list.txt'

def construct_vocab_extended_list_path(num):
    return f'../vocab-lists/{num}/ch{num}-vocab-extended-list.txt'

def construct_vocab_test_path(num, lang):
    return f'../vocab-lists/{num}/ch{num}-vocab-test-{lang}.txt'

def longest_line_length(words, lang, isExtended):
    maxLen = len(words[0][lang])
    for i in range(1, len(words)):
        if isExtended:
            if len(words[i][lang]) > maxLen:
                maxLen = len(words[i][lang])
        else:
            if 'audioFilename' in words[i].keys() and len(words[i][lang]) > maxLen:
                maxLen = len(words[i][lang])
    return maxLen

def list_string_format(maxLatinLen, latinText, englishText):
    i = 0
    msg = ''
    for c in latinText:
        msg += c
        i += 1
    while i < maxLatinLen:
        msg += ' '
        i += 1
    i = 0
    for c in englishText:
        msg += c
    msg += '\n'
    return msg

def test_string_format(maxLen, text):
    i = 0
    msg = ''
    for c in text:
        msg += c
        i += 1
    while i < maxLen:
        msg += ' '
        i += 1
    msg += '=\n'
    return msg    