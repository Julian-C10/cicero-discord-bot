from util import *

async def send_greeting(message):
    await message.channel.send(latin_greeting)

async def send_history(message):
    await message.channel.send(latin_history)

async def send_commands(message):
    await message.channel.send(help_msg)