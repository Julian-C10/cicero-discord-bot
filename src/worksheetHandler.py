import discord
import os.path
from util import standard_error_message

# Sends the self-tutorial exercises for the chapter
async def send_exercises_blank(message, splitMsg, db):
    filePath = construct_exercises_blank_path(splitMsg[1])
    if not(os.path.isfile(filePath)):
        await message.channel.send(standard_error_message)
    else:
        await message.channel.send(file=discord.File(fp=filePath))

# Sends the self-tutorial exercises answer key for the chapter
async def send_exercises_key(message, splitMsg, db):
    filePath = construct_exercises_key_path(splitMsg[1])
    if not(os.path.isfile(filePath)):
        await message.channel.send(standard_error_message)
    else:
        await message.channel.send(file=discord.File(fp=filePath))

# Display a random vocab word in the chapter
async def send_sentences(message, splitMsg, db):
    filePath = construct_sentences_path(splitMsg[1])
    if not(os.path.isfile(filePath)):
        await message.channel.send(standard_error_message)
    else:
        await message.channel.send(file=discord.File(fp=filePath))

def construct_exercises_blank_path(num):
    return f'../worksheets/{num}/ch{num}-self-tutorial-ex.txt'

def construct_exercises_key_path(num):
    return f'../worksheets/{num}/ch{num}-self-tutorial-ex-key.txt'

def construct_sentences_path(num):
    return f'../worksheets/{num}/ch{num}-sententiae.txt'