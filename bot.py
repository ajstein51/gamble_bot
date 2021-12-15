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
########################################################################################################
################################  MONEY COMMANDS  ######################################################
########################################################################################################
# get balance of the user who gave the cmd
@client.command()
async def bal(ctx):
    output = cmd.get_bal(ctx.message.author.id)
    await ctx.send('Money in bank: {0}\tMoney in hand: {1}'.format(output[0], output[1]))
# end of balance function
########################################################################################################
# deposit
@client.command(aliases=['deposit'])
async def dep(ctx, *args):
    if args:
        output = cmd.deposit(ctx.message.author.id, args)
        
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
########################################################################################################
# withdraw
@client.command(aliases=['with'])
async def withdraw(ctx, *args):
    # if we got args
    if args:
        output = cmd.withdraw(ctx.message.author.id, args)
        
        # check the returns
        if output == -1:
            await ctx.send('You didn\'t have that much in your bank account')
        elif output == -2:
            await ctx.send('You didn\'t give me a number')
        else:
            await ctx.send('You have {0} in hand'.format(output))
    else:
        await ctx.send('Didn\'t give the amount')
    # end of if/else
# end of withdraw
########################################################################################################
# get inventory
@client.command(aliases=['inventory'])
async def inv(ctx, *args):
    output = cmd.inv(ctx.message.author.id)
    await ctx.send('You have {0} in your inventory'.format(output[0]))
# end of inventory cmd
########################################################################################################


########################################################################################################
################################  GET MONEY  ###########################################################
########################################################################################################


########################################################################################################
# work, get random money from 25 to 100
@client.command()
async def work(ctx, *args):
    output = cmd.work(ctx.message.author.id)
    await ctx.send('You got {0} amount from working!'.format(output))
# end of work
########################################################################################################
# fish, get random fish from -500 to 1000 amount
@client.command()
async def fish(ctx, *args):
    output = cmd.fish(ctx.message.author.id)
    await ctx.send('You got {0} worth {1} amount!'.format(output[0], output[1]))
# end of fish
########################################################################################################
################################  GAMBLE COMMANDS  #####################################################
########################################################################################################

# get discord token from the environment
load_dotenv()
client.run(os.getenv('TOKEN'))