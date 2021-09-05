import discord
import json
import random
import os.path
from decouple import config
from messages import *
from myWebServer import keep_alive

client = discord.Client()

databasePath = "../database/database.json"

with open(databasePath, 'r', encoding='utf8') as jsonFile:
    db = json.load(jsonFile)

# with open(databasePath, "w") as file:
#     json.dump(data, file)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    splitMsg = message.content.lower().split()

    if message.author == client.user or len(splitMsg) < 1:
        return

    if splitMsg[0] == '!hello':
        await message.channel.send(latin_greeting())

    elif splitMsg[0] == '!history':
        await message.channel.send(latin_history())

    elif splitMsg[0] == 'requests':
        await message.channel.send(help_msg())

    elif (len(splitMsg) >= 4 and splitMsg[0] == 'chapter' and splitMsg[1].isnumeric() and int(splitMsg[1]) >= 1 and 
        int(splitMsg[1]) <= 40 and splitMsg[2] == 'vocab'):
        # List all vocab words in the chapter
        if (splitMsg[3] == 'list'):
            if not(os.path.isfile(construct_vocab_list_path(splitMsg[1]))):
                num = splitMsg[1]
                words = db[f'chapter {splitMsg[1]}']['words']
                longestLineLen = longest_line_length(words)
                msg = ''
                for i in range(0, len(words)):
                    msg += list_string_format(longestLineLen + 5, words[i]['latin'], words[i]['english'])
                with open(construct_vocab_list_path(num), 'w', encoding='utf8') as vocabList:
                    vocabList.write(msg)
            await message.channel.send(file=discord.File(fp=construct_vocab_list_path(splitMsg[1])))

        # Display a random vocab word in the chapter
        elif (splitMsg[3] == 'word'):
            num = splitMsg[1]
            words = db['chapter ' + num]['words']
            index = random.randint(0, len(words) - 1)
            audioFile = words[index]
            filepath = construct_sound_path(num, audioFile['audioFilename'])
            transcript = audioFile['latin'] + '\n' + audioFile['english']
            await message.channel.send(file=discord.File(fp=filepath, filename="audio.mp3"), content=transcript)

def construct_sound_path(num, filename):
    return '../sounds/' + num + '/vocabulary/' + filename

def construct_vocab_list_path(num):
    return f'../vocab-lists/chapter{num}VocabList.txt'

def longest_line_length(words):
    maxLen = len(words[0]['latin'])
    for i in range(1, len(words)):
        if len(words[i]['latin']) > maxLen:
            maxLen = len(words[i]['latin'])
    return maxLen

def list_string_format(maxLatinLen, latinText, englishText):
    englishText = englishText[1:][:-1]
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

keep_alive()
client.run(config('TOKEN'))