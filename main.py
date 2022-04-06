import os

import discord
from commands import *
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

PREFIX = '?'
COMMANDS = {"ping":ping}

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.content.startswith(PREFIX):
        command = message.content.split(' ')[0][len(PREFIX):]
        flags = message.content.split(' ')[1:]
        
        if command in COMMANDS:
            await COMMANDS[command](message, flags)

client.run(TOKEN)
