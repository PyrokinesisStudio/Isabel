import discord
from discord.ext import commands
import subprocess
import asyncio
from subprocess import Popen
import threading
from asyncio.subprocess import PIPE
import aiohttp
from modules.utils.chat_formatting import pagify

class Owner:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shell(self, ctx, *, arg):
        """Shell"""
        proc = await asyncio.create_subprocess_shell(arg, stdin=None, stderr=None, stdout=PIPE)
        out = await proc.stdout.read()
        msg = pagify(out.decode('utf-8'))
        inp = discord.Embed(description="{}".format(ctx.guild), colour=discord.Colour.blue())
        inp.add_field(name="**Input:**", value="`{}`".format(arg))
        await ctx.send(embed=inp)
        for page in msg:
            await ctx.send("```py\n\n{}```".format(page))

def setup(bot):
    bot.add_cog(Owner(bot))
