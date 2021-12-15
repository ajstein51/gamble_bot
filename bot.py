# bot for gambling
# active vm env: source vmenv/bin/activate
# imports
import os # for the token 
import discord
from discord import colour # pip install -U discord.py
from discord.ext import commands
from dotenv import load_dotenv # $ pip install -U python-dotenv
import cmd
import re # pip install regex

# bot prefix
client = commands.Bot(command_prefix='>')
# remove default help command
client.remove_command('help')

# on bot load up
@client.event
async def on_ready():
    print("Bot is online\n".format(client))
    # get global connection to the database
    cmd.start_db()
# end of func

# get balance of the user who gave the cmd
@client.command()
async def bal(ctx):
    output = cmd.get_bal(ctx.message.author.id)
    await ctx.send('Your balance {0} {1}'.format(output[0], output[1]))
# end of balance function

# deposit
@client.command()
async def dep(ctx, *args):
    # get user 
    username = ctx.message.author.id
    print(username)
    
    if args:
        output = cmd.deposit(username, args)
        
        # check for errors
        if output == -1:
            await ctx.send('You don\'t have that much')
        elif output == -2:
            await ctx.send('You didn\'t give me a number')
        else:
            # it worked 
            await ctx.send('You deposited: {0} amount'.format(output))
    else:
        await ctx.send('Didn\'t give the amount')
# end of deposit all

# get discord token from the environment
load_dotenv()
client.run(os.getenv('TOKEN'))