import discord
from discord.ext import commands
import random
from bs4 import BeautifulSoup
import requests
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

class Voicechannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dict = {}
        self.score = {}
        self.host_list = []
        self.currentarticle = None
        self.currenthost = None


    @commands.command()
    async def submit(self, ctx, article):
        await ctx.send("Submitted article.")
        self.dict[ctx.author.id] = article



    @commands.command()
    async def roundstart(self, ctx):
        if not self.host_list:
            self.host_list = generateHostList(self)
        self.currenthost = next(iter(self.host_list))
        self.host_list.remove(self.currenthost)
        self.hostarticle = self.dict.pop(self.currenthost)
        try:
            self.currentarticle = random.choice(list(self.dict.values()))
        except IndexError:
            await ctx.send("Submit articles first.")
            self.dict[self.currenthost] = self.hostarticle
            return
        self.dict[self.currenthost] = self.hostarticle

        response = requests.get(self.currentarticle)
        soup = BeautifulSoup(response.content, 'lxml')
        title = soup.find(id='firstHeading').get_text()
        await ctx.send(f"The article is `{title}` The host is {ctx.guild.get_member(self.currenthost).display_name}`.")

    @commands.command()
    async def choose(self, ctx, *, member: discord.Member):
        if ctx.author.id != self.currenthost:
            await ctx.send("You are not the host.")
            return
        id = get_key(self, self.currentarticle)
        if member.id == id:
            await ctx.send("That is correct! Adding points.")
            if ctx.author.id in self.score:
                self.score[ctx.author.id] += 1
            else:
                self.score[ctx.author.id] = 1
            if ctx.author.id in self.score:
                self.score[id] += 1
            else:
                self.score[id] = 1
        else:
            await ctx.send(f"Not correct. You are bad. The real article was {ctx.guild.get_member(id).display_name}'s.")

        self.dict.pop(get_key(self, self.currentarticle))

    @commands.command()
    async def score(self, ctx):
        scorelist = ""
        if not self.score:
            await ctx.send("There are no scores.")
            return
        for id in self.score:
            scorelist += (f"\n{ctx.guild.get_member(id)}: {self.score[id]}")
        await ctx.send(scorelist)

    @commands.command()
    async def forfeit(self, ctx):
        self.dict.pop(ctx.author.id)
        await ctx.send("Removed you from the game.")

    @commands.command()
    async def reset(self, ctx):
        self.dict.clear()
        self.score.clear()
        await ctx.send("Cleared game data.")

    @commands.command()
    async def remove(self, ctx, member : discord.Member):
        self.dict.pop(member.id)
        try:
           self.score.pop(member.id)
        except IndexError:
            self.score.pop(member.id)
        await ctx.send(f"Removing {member.displayname} from the game.")

def generateHostList(slf):
    hosts = []
    for id in slf.dict:
        hosts.append(id)
    return hosts


def get_key(self, val):
    for key, value in self.dict.items():
        if val == value:
            return key
def setup(bot):
    bot.add_cog(Voicechannel(bot))