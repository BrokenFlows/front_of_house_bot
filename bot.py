#! /usr/local/bin/python3

import config
import discord
from discord.ext import commands

description = """The face of the bot working behind the scenes"""
bot = commands.Bot(command_prefix=config.prefix, description=description)

# declare when the bot is running
@bot.event
async def on_ready():
    print('Logged in as', end=" ")
    print(bot.user.name)

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
    await ctx.send('{:3d} ms'.format(latency))

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

bot.run(config.token)

