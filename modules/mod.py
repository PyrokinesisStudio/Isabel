import discord
from discord.ext import commands

class Mod:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(no_pm=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member=None, *, reason: str=None):
        """Bans a user and deletes the last 7 days worth of their messages."""
        author = ctx.author
        guild = ctx.guild
        if user is None:
            await ctx.send(f"You need to mention a user to ban.\n`{ctx.prefix}ban @user`")
            return
        if author is user:
            await ctx.send("Baka, don't ban yourself!")
            return
        if reason is None:
            try:
                await guild.ban(user, reason=f"[{author.name}] - No reason was specified.", delete_message_days=7)
            except discord.Forbidden:
                await ctx.send("I'm not allowed to do that.")
            else:
                await ctx.send(f"I banned them, senpai~{author.name}! :blush:")
        else:
            try:
                await guild.ban(user, reason=f"[{author.name}] - {reason}", delete_message_days=7)
            except discord.Forbidden:
                await ctx.send("I'm not allowed to do that.")
            else:
                await ctx.send(f"I banned them, senpai~{author.name}! :blush:")
    
    @commands.command(no_pm=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member=None, *, reason: str=None):
        """Kicks a user."""
        author = ctx.author
        guild = ctx.guild
        if user is None:
            await ctx.send(f"You need to mention a user to kick.\n`{ctx.prefix}kick @user`")
            return
        if author is user:
            await ctx.send("Baka, don't kick yourself!")
            return
        if reason is None:
            try:
                await guild.kick(user, reason=f"[{author.name}] - No reason was specified.")
            except discord.Forbidden:
                await ctx.send("I'm not allowed to do that.")
            else:
                await ctx.send(f"I kicked them, senpai~{author.name}! :blush:")
        else:
            try:
                await guild.kick(user, reason=f"[{author.name}] - {reason}")
            except discord.Forbidden:
                await ctx.send("I'm not allowed to do that.")
            else:
                await ctx.send(f"I kicked them, senpai~{author.name}! :blush:")

def setup(bot):
    bot.add_cog(Mod(bot))
