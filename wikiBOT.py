import discord, re, asyncio
from os import environ
from wiki import Wiki

client = discord.Client()
TOKEN = 'TOKEN_NUMBER_HERE'

@client.event
async def on_ready():
    print('Logged in as %s' % client.user.name)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!wiki'):
        content = message.content[5:]
        content = re.sub('\s','_',content)
        w = Wiki(content)
        response = w.getSum()
        await message.channel.send(response)
        if 'more at' not in response:
            await message.channel.send('Wanna see more information?(y/n)')
            msg = await client.wait_for('message')
            if msg.content == 'y':
                await message.channel.send('See more at ' + w.getLink())

client.run(TOKEN)
