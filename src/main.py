import discord
import json
import random
import os.path
import time
import sys
from decouple import config
from myWebServer import keep_alive
from miscHandler import *
from vocabHandler import *
from worksheetHandler import *
from cache import *
from util import databasePath

client = discord.Client()

with open(databasePath, 'r', encoding='utf8') as jsonFile:
    db = json.load(jsonFile)

shouldProfile = False

if len(sys.argv) > 1 and '-p' in sys.argv:
    shouldProfile = True

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global db
    if shouldProfile:
        start_time = time.process_time()

    if db_is_changed():
        clear_lists()
        with open(databasePath, 'r', encoding='utf8') as jsonFile:
            db = json.load(jsonFile)
    
    splitMsg = message.content.lower().split()

    if message.author == client.user or len(splitMsg) < 1 or (type(message.channel) is discord.TextChannel and message.channel.name == 'suggestions'):
        return

    if splitMsg[0] == 'hello':
        await send_greeting(message)

    elif len(splitMsg) == 2 and splitMsg[0] == 'latin' and splitMsg[1] == 'history':
        await send_history(message)

    elif len(splitMsg) == 2 and splitMsg[0] == 'bot' and splitMsg[1] == 'commands':
        await send_commands(message)

    elif (len(splitMsg) >= 3 and splitMsg[0] == 'chapter' and splitMsg[1].isnumeric() and 
        int(splitMsg[1]) >= 1 and int(splitMsg[1]) <= 40):
        # List all vocab words in the chapter
        if len(splitMsg) == 5 and splitMsg[2] == 'vocab' and splitMsg[3] == 'extended' and splitMsg[4] == 'list':
            await send_vocab_extended_list(message, splitMsg, db)

        # List all vocab words with an audio file in the chapter
        elif len(splitMsg) == 4 and splitMsg[2] == 'vocab' and splitMsg[3] == 'list':
            await send_vocab_list(message, splitMsg, db)

        # Display a random vocab word in the chapter
        elif len(splitMsg) == 4 and splitMsg[2] == 'vocab' and splitMsg[3] == 'word':
            await send_random_word(message, splitMsg, db)

        # Display a specific vocab word in the chapter
        elif len(splitMsg) == 5 and splitMsg[2] == 'vocab' and splitMsg[3] == 'word':
            await send_specific_word(message, splitMsg, db)

        # List all vocab words in chapter in one language
        elif len(splitMsg) == 5 and splitMsg[2] == 'vocab' and splitMsg[3] == 'test' and splitMsg[4] in languages:
            await send_vocab_test(message, splitMsg, db)

        elif len(splitMsg) == 3 and splitMsg[2] == 'exercises':
            await send_exercises_blank(message, splitMsg, db)

        elif len(splitMsg) == 4 and splitMsg[2] == 'exercises' and splitMsg[3] == 'key':
            await send_exercises_key(message, splitMsg, db)

        elif len(splitMsg) == 3 and splitMsg[2] == 'sentences':
            await send_sentences(message, splitMsg, db)
    
    if shouldProfile:
        elapsed_time = time.process_time() - start_time
        print("elapsed time: %.9fs" % elapsed_time)

keep_alive()
client.run(config('TOKEN'))