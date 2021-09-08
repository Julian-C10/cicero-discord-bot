import discord
import json
import random
import os
import time
import sys
from decouple import config
from myWebServer import keep_alive
from vocabHandler import *
from worksheetHandler import *
from cache import *
from util import *

client = discord.Client()

with open(databasePath, 'r', encoding='utf-8') as jsonFile:
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
        with open(databasePath, 'r', encoding='utf-8') as jsonFile:
            db = json.load(jsonFile)
    
    splitMsg = message.content.lower().split()

    if message.author == client.user or len(splitMsg) < 1 or (type(message.channel) is discord.TextChannel and message.channel.name == 'suggestions'):
        return

    if splitMsg[-1][-1] in '!?.,;':
        splitMsg[-1] = splitMsg[-1][:-1]

    if len(splitMsg) == 2 and (splitMsg[0] == 'hello' or splitMsg[0] == 'hi') and splitMsg[1] == 'cicero':
        await message.channel.send(latin_greeting)

    if len(splitMsg) == 1 and splitMsg[0] == 'cicero':
        await message.channel.send(help_msg)

    elif len(splitMsg) == 2 and splitMsg[0] == 'latin' and splitMsg[1] == 'history':
        await message.channel.send(latin_history_error)

    elif len(splitMsg) == 3 and splitMsg[0] == 'latin' and splitMsg[1] == 'history' and splitMsg[2] == 'wheelock':
        await message.channel.send(latin_history_wheelock)

    elif len(splitMsg) == 3 and splitMsg[0] == 'latin' and splitMsg[1] == 'history' and splitMsg[2] == 'wikipedia':
        await message.channel.send(latin_history_wikipedia)

    elif len(splitMsg) >= 3 and splitMsg[0] == 'chapter' and splitMsg[1].isnumeric():
        if int(splitMsg[1]) < 1 or int(splitMsg[1]) > 40:
            await message.channel.send(chapter_num_out_of_range_error(splitMsg[1]))
        
        elif len(splitMsg) == 3 and splitMsg[2] == 'vocab':
            await message.channel.send(vocab_missing_command(splitMsg[1]))

        elif len(splitMsg) == 4 and splitMsg[2] == 'vocab' and splitMsg[3] == 'test':
            await message.channel.send(vocab_test_missing_command(splitMsg[1]))

        # List all vocab words with an audio file in the chapter
        elif len(splitMsg) == 4 and splitMsg[2] == 'vocab' and splitMsg[3] == 'list':
            await send_vocab_list(message, splitMsg, db)

        # Display a random vocab word in the chapter
        elif len(splitMsg) == 4 and splitMsg[2] == 'vocab' and splitMsg[3] == 'word':
            await send_random_word(message, splitMsg, db)

        # Display a specific vocab word in the chapter
        elif len(splitMsg) >= 5 and len(splitMsg) < 20 and splitMsg[2] == 'vocab' and splitMsg[3] == 'word':
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

#keep_alive()
if 'TOKEN' in os.environ:
    token = os.environ['TOKEN']
else:
    token = config('TOKEN')

client.run(token)