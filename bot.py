#! /usr/local/bin/python3

import config
import discord
from discord.ext import commands

description = """Runs the show around here"""
bot = commands.Bot(command_prefix=config.prefix, description=description)

@bot.event
async def on_ready():
    print('Logged in as', end=" ")
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def hello(ctx):
    """Says world"""
    await ctx.send("world")

@bot.command()
async def ping(ctx):
    """Gets the bot's latency"""
    # Get the latency of the bot
    latency = bot.latency 
    # Send it to the user
    await ctx.send(latency)

@bot.command()
async def echo(ctx, *, source : str):
    """Echoes the phrase back to the sender"""
    await ctx.send(source)

bot.run(config.token)

