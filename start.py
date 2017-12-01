from discord.ext import commands
import discord

import asyncio
import aiohttp
import random
import string
import os
import datetime
import json

with open("config.json") as conf:
    config = json.load(conf)
    token = config["token"]
    prefix = config["prefix"]
    description = config["description"]
    log_channel_id = config["log_channel_id"]
    playing_status = config["playing_status"]

class Core:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, name: str):
        """Reloads module"""
        try:
            self.bot.unload_extension(f"modules.{name}")
            self.bot.load_extension(f"modules.{name}")
        except Exception as e:
            await ctx.send(f"```\n{e}```")
            return
        await ctx.send(f"Reloaded module **{name}.py**")

    @commands.command(description="Unloads an extension")
    @commands.is_owner()
    async def unload(self, ctx, name: str):
        """Unloads module"""
        try:
            self.bot.unload_extension(f"modules.{name}")
            print(f"Unloading module {name}")
        except Exception as e:
            await ctx.send(f"```\n{e}```")
            return
        await ctx.send(f"Unloaded module {name}")

    @commands.command(description="loads an extension")
    @commands.is_owner()
    async def load(self, ctx, name: str):
        """Load module"""
        try:
            self.bot.load_extension(f"modules.{name}")
        except Exception as e:
            await ctx.send(f"```\n{e}```")
            return
        await ctx.send(f"Loaded module **{name}.py**")

    @commands.command(no_pm=True)
    @commands.is_owner()
    async def modules(self, ctx):
        """Modules"""
        list = []
        for file in os.listdir("./modules"):
            if file.endswith(".py"):
                list.extend([f"{file}"])
        await ctx.send(list)

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or(prefix),
                   description=description)

@bot.event
async def on_ready():
    print("Logged in as {0.id}/{0}".format(bot.user))
    print(f"{bot.shard_count}")
    print("----------")
    for file in os.listdir("modules"):
        if file.endswith(".py"):
            name = file[:-3]
            try:
                bot.load_extension(f"modules.{name}")
            except:
                owner = await self.bot.get_user_info(209137943661641728)
                await owner.send(f"{name} failed to load! :warning:")
    while True:
        await bot.change_presence(game=discord.Game(name=f"{playing_status} | {len(bot.guilds)} Guilds"))
        await asyncio.sleep(600)

@bot.event
async def on_guild_join(guild):
    channel = bot.get_channel(log_channel_id)
    em = discord.Embed(title="Joined Guild", color=discord.Color.green())
    avatar = bot.user.avatar_url if bot.user.avatar else bot.user.default_avatar_url
    em.set_author(name=guild.name, icon_url=avatar)
    em.set_thumbnail(url=guild.icon_url)
    em.add_field(name="Total Users", value=len(guild.members))
    em.add_field(name="Guild Owner", value=str(guild.owner))
    em.add_field(name="Total Guilds", value=len(bot.guildss))
    em.set_footer(text="Guild ID: " + guild.id)
    await channel.send(embed=em)

@bot.event
async def on_guild_remove(guild):
    channel = bot.get_channel(log_channel_id)
    em = discord.Embed(title="Left Guild", color=discord.Color.red())
    avatar = bot.user.avatar_url if bot.user.avatar else bot.user.default_avatar_url
    em.set_author(name=guild.name, icon_url=avatar)
    em.set_thumbnail(url=guild.icon_url)
    em.add_field(name="Total Guilds", value=len(bot.guilds))
    em.add_field(name="Owner", value=str(guild.owner))
    em.set_footer(text="Guild ID: " + guild.id)
    await channel.send(embed=em)
    
@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        channel = bot.get_channel(log_channel_id)
        time = datetime.datetime.now()
        fmt = '[ %H:%M:%S ] %d-%B-%Y'
        author = message.author
        avatar = message.author.avatar_url if message.author.avatar else bot.user.default_avatar_url
        em = discord.Embed(title='DM', colour=discord.Colour.blue())
        em.set_author(name=f"{author}", icon_url=avatar)
        em.set_thumbnail(url=avatar)
        em.add_field(name="Message ID", value=message.id)
        em.add_field(name="User ID", value=author.id)
        em.add_field(name="Channel", value=message.channel)
        em.add_field(name="Message", value=message.content)
        em.set_footer(text=time.strftime(fmt), icon_url='http://orig08.deviantart.net/5d90/f/2016/099/d/a/discord_token_icon_light_by_flexo013-d9y9q3w.png')
        await channel.send(embed=em)
        
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, err):
    if isinstance(err, commands.CommandNotFound):
        return
    await ctx.send(f"```\n{err}\n```")
    print(err)

bot.add_cog(Core(bot))
bot.run(token)
