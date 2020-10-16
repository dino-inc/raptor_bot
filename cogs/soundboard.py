import discord
from discord.ext import commands
class Soundboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voiceclient = None

    @commands.command()
    async def connect(self, ctx, *, channel : discord.VoiceChannel):
        self.voiceclient = await channel.connect()

    @commands.command()
    async def disconnect(self, ctx):
        await self.voiceclient.disconnect()

    

def setup(bot):
    bot.add_cog(Soundboard(bot))