import discord
import time
import sys, traceback
from discord.ext import commands
import configparser
import os

bot = commands.Bot(command_prefix='!')
initial_extensions = ['cogs.voicechannel', 'cogs.twoliars']

#generating the config if none is found, with default values
botconfig = configparser.ConfigParser()
if not os.path.exists('config.ini'):
    print("No config file found, regenerating config.ini.")

    botconfig['General'] = {'use_test_guild': 'True',
                            'enabled': 'True'}

    botconfig['GrandCountry'] = {'guild_id': '187011562337337344',
                                 'voicechannel_id': '224382963997999104',
                                 'botchannel_id': '402250945519419412'}

    botconfig['TestServer'] = {'guild_id': '277294377548775425',
                                'voicechannel_id': '277294377548775426',
                               'botchannel_id': '401057950510350338'}

    botconfig['GameData'] = {'Warframe': '4'}

    with open('config.ini', 'w') as configfile:
        botconfig.write(configfile)

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


#add in if config necessary in this main file
#botconfig.read('config.ini')

@bot.event
async def on_connect():
    print("Connected to Discord.")

@bot.event
async def on_ready():
    print(discord.__version__)
    print('Logged on as {0}!'.format(bot.user.name))
    print('Servers: ', end ='')
    for guild in bot.guilds:
        print(str('{0}, ').format(guild), end='')
    print()
    print("------------------------------")

 
# dino_bot
token = open("token.txt", 'r')
token = token.read().strip()
bot.run(token, bot=True, reconnect=True)

