#! /usr/local/bin/python3 -u

import config
import discord
import re
from datetime import datetime
from discord.ext import commands
from inspect import signature

def log_call(func):
    async def wrapped_in(*def_args, **kwdef_args):
        print("Registered command: ", func.__name__)
        res = await func(*def_args, **kwdef_args)
        return res

    params = signature(func).parameters
    params = [str(p) for p in params.values()]
    def_args = ",".join(params)

    params = signature(func).parameters
    params = [p.name for p in params.values()]
    call_args = ",".join(params)
    print(def_args)
    definition = f"""async def wrapped({def_args}):
    res = await wrapped_in({call_args})
    return res
    """
    print(definition)

    fakelocals = {}
    exec(definition, {"wrapped_in": wrapped_in}, fakelocals)
    wrapped = fakelocals['wrapped']

    wrapped.__name__ = func.__name__

    return wrapped

# to add version numbers to the bot as to track of which commit is running
try:
    with open('/home/pi/production/front_of_house_bot/.version', 'r') as version_file:
        version = version_file.read()
except:
    version = "unknown"

description = f"""The face of the bot working behind the scenes\nVersion {version}"""
bot = commands.Bot(command_prefix=config.prefix, description=description)

# declare when the bot is running
@bot.event
async def on_ready():
    print(f'{datetime.now()}: Logged in as {bot.user.name} version {version}')

# check if it can hear you, in a kinda cute way
@bot.command()
@log_call
async def hello(ctx):
    """Says world, get it?"""
    await ctx.send("world")

# sends the ping of the bot to the asking channel
@bot.command()
@log_call
async def ping(ctx):
    """Gets the bot's latency in ms"""
    # Get the latency of the bot
    await ctx.send(int(round(bot.latency, 3) * 1e3))#f'{ltnc:3d} ms')

# echo back a command
@bot.command()
@log_call
async def echo(ctx, *, source : str):
    """Echoes the phrase back to the sender"""
    await ctx.send(source)

# echo back the command with tts
@bot.command()
@log_call
async def tts(ctx, *, source : str):
    """Echoes the phrase back using TTS"""
    # tts flag means the client while read it aloud
    await ctx.send(source, tts=True)

# echo back a command
@bot.command()
@log_call
async def puppet(ctx, *, source : str):
    """Deletes the command message then repeats it"""
    message = ctx.message
    if (message.author.id == config.puppet_master):
        await message.delete()
        await ctx.send(source)

# move a command to a different channel
@bot.command()
@log_call
async def move(ctx, other_user : str, other_channel : str):
    """Deletes the chosen message and moves it to another channel"""
    print(f'{type(ctx)}, {ctx}')
    print(f'{type(other_user)}, {other_user}')
    print(f'{type(other_channel)}, {other_channel}')
    other_user_id = int(re.search(r'\d+', other_user).group(0))
    other_channel_id = int(re.search(r'\d+', other_channel).group(0))
    print(f'{type(other_user_id)}, {other_user_id}')
    print(f'{type(other_channel_id)}, {other_channel_id}')
#    message = ctx.message
#    if (message.author.id == config.puppet_master):
#        await message.delete()
#        await ctx.send(source)

bot.run(config.token)

