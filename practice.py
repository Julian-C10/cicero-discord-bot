
def practice_test(num):
    item = audioFiles['shortA']
    filepath = "sounds\\" + item[0]
    transcript = "Transcript: " + item[1]
    await message.channel.send(file=discord.File(filepath), content=transcript)