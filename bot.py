#! /usr/local/bin/python3

import config
import discord
import re
from datetime import datetime
from discord.ext import commands

# to add version numbers to the bot as to track of which commit is running
try:
    with open('/home/pi/production/front_of_house_bot/.version', 'r') as version_file:
        version = version_file.read()
except:
    version = "unknown"

description = f"""The face of the bot working behind the scenes\nVersion {version} {id(version)}"""
bot = commands.Bot(command_prefix=config.prefix, description=description)

# declare when the bot is running
@bot.event
async def on_ready():
    print(f'{datetime.now()}: Logged in as {bot.user.name} version {version} {id(version)}')

# check if it can hear you, in a kinda cute way
@bot.command()
async def hello(ctx):
    """Says world, get it?"""
    await ctx.send("world")

# sends the ping of the bot to the asking channel
@bot.command()
async def ping(ctx):
    """Gets the bot's latency in ms"""
    # Get the latency of the bot
    latency = int(round(bot.latency, 3) * 1e3)
    # tell the user
    await ctx.send(f'{latency:3d} ms')

# echo back a command
@bot.command()
async def echo(ctx, *, source : str):
    """Echoes the phrase back to the sender"""
    await ctx.send(source)

# echo back the command with tts
@bot.command()
async def tts(ctx, *, source : str):
    """Echoes the phrase back using TTS"""
    # tts flag means the client while read it aloud
    await ctx.send(source, tts=True)

# echo back a command
@bot.command()
async def puppet(ctx, *, source : str):
    """Deletes the command message then repeats it"""
    message = ctx.message
    if (message.author.id == config.puppet_master):
        await message.delete()
        await ctx.send(source)

# move a command to a different channel
@bot.command()
async def move(ctx, other_user : str, other_channel : str):
    """Deletes the chosen message and moves it to another channel"""
    print(f'{type(ctx)}, {ctx}')
    print(f'{type(other_user)}, {other_user}')
    print(f'{type(other_channel)}, {other_channel}')
    other_user_id = int(re.search(r'\d*', other_user).group(0))
    other_channel_id = int(re.search(r'\d*', other_channel).group(0))
    print(f'{type(other_user_id)}, {other_user_id}')
    print(f'{type(other_channel_id)}, {other_channel_id}')
#    message = ctx.message
#    if (message.author.id == config.puppet_master):
#        await message.delete()
#        await ctx.send(source)

bot.run(config.token)

