import discord
import random
import os.path
from util import *

async def send_vocab_list(message, splitMsg, db):
    filePath = construct_vocab_list_path(splitMsg[1])
    dirPath = construct_vocab_dir_path(splitMsg[1])
    vocabPath = construct_vocab_path()
    if not(os.path.isfile(filePath)):
        num = splitMsg[1]
        words = db[f'chapter {splitMsg[1]}']['words']
        if 'latin' not in words[0].keys():
            await message.channel.send(standard_error_message)
            return
        longestLineLen = longest_line_length_util(words, 'latin')
        msg = ''
        for i in range(0, len(words)):
            if 'audioFilename' in words[i].keys():
                msg += list_string_format(longestLineLen + 5, words[i]['latin'], words[i]['english'])
        msgList = msg.split("\n")
        msgList = sorted(msgList, key=str.casefold)
        msg = "\n".join(msgList)
        if not os.path.isdir(vocabPath):
            os.mkdir(vocabPath)
        if not os.path.isdir(dirPath):
            os.mkdir(dirPath)
        with open(filePath, 'w', encoding='utf8') as vocabList:
            vocabList.write(msg)
    await message.channel.send(file=discord.File(fp=filePath))

# List all vocab words in chapter in one language
async def send_vocab_test(message, splitMsg, db):
    desiredLang = splitMsg[4]
    filePath = construct_vocab_test_path(splitMsg[1], desiredLang)
    dirPath = construct_vocab_dir_path(splitMsg[1])
    vocabPath = construct_vocab_path()
    if not(os.path.isfile(filePath)):
        num = splitMsg[1]
        words = db[f'chapter {splitMsg[1]}']['words']
        if 'latin' not in words[0].keys():
            await message.channel.send(standard_error_message)
            return
        longestLineLen = longest_line_length_util(words, desiredLang)
        msg = ''
        for i in range(0, len(words)):
            if 'audioFilename' in words[i].keys():
                msg += test_string_format(longestLineLen + 1, words[i][desiredLang])
        msgList = msg.split("\n")
        msgList = sorted(msgList, key=str.casefold)
        msg = "\n".join(msgList)
        if not os.path.isdir(vocabPath):
            os.mkdir(vocabPath)
        if not os.path.isdir(dirPath):
            os.mkdir(dirPath)
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
    desiredWords = splitMsg[4:]
    words = db[f'chapter {num}']['words']
    if 'latin' not in words[0].keys():
        await message.channel.send(standard_error_message)
        return
    index = -1
    for i in range(0, len(words)):
        found = True
        for desiredWord in desiredWords:
            if desiredWord not in words[i]['latin'] and desiredWord not in words[i]['english']:
                found = False
                break
        if found:
            index = i
            break
    if index == -1:
        reconstructedMsg = ' '.join(desiredWords)
        await message.channel.send(missing_specific_vocab_word_error(reconstructedMsg, num))
    else:
        word = words[index]
        transcript = f"{word['latin']}\n*{word['english']}*"
        if 'audioFilename' in word.keys():
            filepath = construct_sound_path(num, word['audioFilename'])
            await message.channel.send(file=discord.File(fp=filepath, filename="audio.mp3"), content=transcript)
        else:
            await message.channel.send(transcript)

# Display a specific vocab word in the chapter
async def send_specific_word_all_chapters(message, splitMsg, db):
    desiredWords = splitMsg[2:]
    index = -1
    for num in range(1, 41):
        words = db[f'chapter {num}']['words']
        foundWords = False
        for i in range(0, len(words)):
            found = True
            for desiredWord in desiredWords:
                latinText = words[i]['latin'].lower()
                englishText = words[i]['english'].lower()
                if desiredWord not in latinText and desiredWord not in englishText:
                    found = False
                    break
            if found:
                index = i
                foundWords = True
                break
        if foundWords:
            break
        
    if index == -1:
        reconstructedMsg = ' '.join(desiredWords)
        await message.channel.send(missing_specific_vocab_word_all_chapters_error(reconstructedMsg))
    
    else:
        word = words[index]
        transcript = f"chapter {num}\n{word['latin']}\n*{word['english']}*"
        if 'audioFilename' in word.keys():
            filepath = construct_sound_path(num, word['audioFilename'])
            await message.channel.send(file=discord.File(fp=filepath, filename="audio.mp3"), content=transcript)
        else:
            await message.channel.send(transcript)

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