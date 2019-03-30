import discord
from discord.ext import commands
import configparser

botconfig = configparser.ConfigParser()
botconfig.read('config.ini')

class Voicechannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global vc
        discord_ids = await setup_config()
        server = self.bot.get_guild(int(discord_ids['guild_id']))
        vc = server.get_channel(int(discord_ids['voicechannel_id']))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # checks when a user joins the voicechannel
        if before.channel is None and after.channel == vc:
            await check_member_games(member,vc)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):

        if after not in vc.members:
            return
        if after is None:
            return
        current_game = (after.activity.name).lower()
        # checks when a user in the voicechannel changes games
        try:
            if current_game in botconfig['GameData']:
                await check_member_games(after, vc)
        except KeyError:
            print(f"person is playing undetected {current_game}")

    @commands.command()
    async def addgame(self, ctx, game_string, squad_size):
        if ctx.author.id == 141695444995670017:
            try:
                if int(botconfig['GameData'][game_string]) != squad_size:
                    botconfig.set('GameData', str(game_string), str(squad_size))
                    with open('config.ini', 'w') as configfile:
                        botconfig.write(configfile)
                    discord_ids = await setup_config()
                    server = self.bot.get_guild(int(discord_ids['guild_id']))
                    bot_channel = server.get_channel(int(discord_ids['botchannel_id']))
                    await bot_channel.send(f"Changed {game_string} to a maximum party size of {squad_size}.")
                    return
                await cxt.send("Game already in config.")
            except KeyError:
                botconfig.set('GameData', str(game_string), str(squad_size))
                with open('config.ini', 'w') as configfile:
                    botconfig.write(configfile)
                discord_ids = await setup_config()
                server = self.bot.get_guild(int(discord_ids['guild_id']))
                bot_channel = server.get_channel(int(discord_ids['botchannel_id']))
                await bot_channel.send(f"Added {game_string} with a maximum party size of {squad_size}.")
        else:
            ctx.send("No.")

    @commands.command()
    async def toggle_flex(self, ctx):
        if ctx.message.author.id == 141695444995670017:
            if botconfig['General'].getboolean('enabled'):
                await ctx.send("Disabling flex voice channel.")
                botconfig.set('General', 'enabled', 'False')
                with open('config.ini', 'w') as configfile:
                    botconfig.write(configfile)
            else:
                await ctx.send("Enabling flex voice channel.")
                botconfig.set('General', 'enabled', 'True')
                with open('config.ini', 'w') as configfile:
                    botconfig.write(configfile)
        else:
            ctx.send("No.")

    @commands.command()
    async def toggle_test_server(self, ctx):
        if ctx.message.author.id == 141695444995670017:
            if botconfig['General'].getboolean('use_test_guild'):
                await ctx.send("Switching to the Grand Country.")
                botconfig.set('General', 'enabled', 'False')
                with open('config.ini', 'w') as configfile:
                    botconfig.write(configfile)
            else:
                await ctx.send("Switching to test server.")
                botconfig.set('General', 'enabled', 'True')
                with open('config.ini', 'w') as configfile:
                    botconfig.write(configfile)
        else:
            ctx.send("No.")

async def check_member_games(member, vc):
    if botconfig['General'].getboolean('enabled'):
        if member.activity is None:
            return
        else:
            await vc.edit(user_limit=botconfig['GameData'][member.activity.name])


async def setup_config():
    with open('config.ini', 'w') as configfile:
        botconfig.write(configfile)
    if botconfig['General'].getboolean('use_test_guild'):
        discord_ids = botconfig['TestServer']
    else:
        discord_ids = botconfig['GrandCountry']
    return discord_ids

def setup(bot):
    bot.add_cog(Voicechannel(bot))