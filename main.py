import discord
import json
import random
from decouple import config
from messages import *

client = discord.Client()

databaseFilename = "database/database.json"

with open(databaseFilename, 'r', encoding='utf8') as json_file:
    db = json.load(json_file)

# with open(databaseFilename, "w") as file:
#     json.dump(data, file)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    splitMsg = message.content.lower().split()

    if message.author == client.user:
        return

    if splitMsg[0] == '!hello':
        await message.channel.send(latin_greeting())

    elif splitMsg[0] == '!history':
        await message.channel.send(latin_history())

    elif splitMsg[0] == '!help' or splitMsg[0] == '!':
        await message.channel.send(help_msg())

    elif (splitMsg[0] == 'chapter' and splitMsg[1].isnumeric() and splitMsg[2] == 'vocab' and splitMsg[3] == 'word' or
          splitMsg[0] == '!p' and splitMsg[1].isnumeric()):
        num = str(splitMsg[1])
        audioFiles = db['chapter ' + num]['audioFiles']
        index = random.randint(0, len(audioFiles) - 1)
        audioFile = audioFiles[index]
        filepath = 'sounds/' + num + '/vocabulary/' + audioFile['audioFilename']
        transcript = audioFile['latin'] + '\n' + audioFile['english']
        await message.channel.send(file=discord.File(fp=filepath, filename="unknown.mp3"), content=transcript)

    elif message.content.startswith('$pronounce'):
        if 'short a' in message.content:
            item = audioFiles['shortA']
            filepath = "sounds\\" + item[0]
            transcript = "Transcript: " + item[1]
            await message.channel.send(file=discord.File(filepath), content=transcript)

    # elif message.content.startswith('!test'):
    #     if isSoundTest():
    #         if hasValidatedNumber():
    #             launchSoundTestWithChapter()
    #     elif isTranslateTest():
    #         if hasValidatedNumber():
    #             launchSoundTestWithChapter()

client.run(config('TOKEN'))