#! /usr/local/bin/python3

import config
import json
import discord
from discord.ext import commands

def get_emoji_rules_json():
    with open('emoji_roles.json', 'r') as erfile:
        data=erfile.read()
    
    erobj = json.loads(data)
    
    return erobj

# need members intent to get any member info, such as list
intents = discord.Intents.default()
intents.members = True

#START_MESSAGE = 764867821065863200

# setup with above intents
client = discord.Client(intents=intents)

# when bot online
@client.event
async def on_ready():
    print("Client logged in")

# when there is a reaction
@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    erobj = get_emoji_rules_json()
    if (str(message_id) in erobj): # check that it's only on a specific message
        erdct = erobj[str(message_id)]

        # make sure it's in the same server
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        # only assign role if it's a check emoji
        if (payload.emoji.name == erdct["emoji"]):
            role = discord.utils.get(guild.roles, name=erdct["role"])

            # verify the member is in the server
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role) # let's fucking go

# same as above but for revoking membership
@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    erobj = get_emoji_rules_json()
    if (str(message_id) in erobj):
        erdct = erobj[str(message_id)]

        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if (payload.emoji.name == erdct["emoji"]):
            role = discord.utils.get(guild.roles, name=erdct["role"])

            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)

# start that bot
client.run(config.token)

