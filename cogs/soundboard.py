import discord
from discord.ext import commands
class Soundboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def beep(self, ctx, article):
        await ctx.send("Beep.")

def setup(bot):
    bot.add_cog(Soundboard(bot))