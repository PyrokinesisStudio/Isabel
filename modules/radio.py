from discord.ext import commands
import discord
import asyncio
import sharedstream
from modules.utils.sharedstream import sharedstream
import aiohttp
import os
import psutil
import shutil
import xmltodict
import json

stream = sharedstream.SharedFFmpegStream(source='https://stream.radioharu.pw/owo')

class Radio:
    """Radio Haru - www.RadioHaru.pw"""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
    
    @commands.command(no_pm=True)
    async def play(self, ctx):
        """Play"""
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.send(f"Already connected to a voice channel, use `{ctx.prefix}stop` to change voice channel.")
        else:
            vc = await channel.connect()
            vc.play(stream)
            await ctx.send(":green_heart: **Playing Radio Haru!**")
    
    @commands.command(no_pm=True)
    async def stop(self, ctx):
        """Stop"""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send(":red_circle: **Stopped playing Radio Haru!**")
        else:
            await ctx.send("Not in a voice channel.")
        
    @commands.command(no_pm=True)
    async def song(self, ctx):
        """Currently playing song."""
        async with self.session.get("https://stream.radioharu.pw/status-json.xsl") as resp:
            data = await resp.json()
            song = data["icestats"]["source"]["title"]
            
        embed = discord.Embed(description="Currently Playing", colour=discord.Colour.blue())
        embed.add_field(name="Song: ", value=f"**{song}**")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Radio(bot))
