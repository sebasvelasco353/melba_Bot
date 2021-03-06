import os
import random
import discord
from discord.ext import commands

USER = os.getenv('MELBA_BOT')
CRYPTO_C = os.getenv('CRYPTO_CHANNEL')
client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
   print('We are logged in as {0.user}'.format(client))

@client.event
async def on_member_join(member):
    print('hello new user')

@client.command()
async def cmds(ctx):
    await ctx.send('Mijo, the commands are: \n!melbaTip <--- ask me anything mijo.\n!cryptoMelba <--- i tell you about crypto coins')

@client.command()
async def melbaTip(ctx, *, question):
    responses = [
        'Dont do it, mijo...',
        'pailander... that means no',
        'you should know',
        'yeah, get that sweet sweet victory',
        'do what you must',
        'remember, with great power comes great responsability',
        'Read the manual',
        'Have you tried turning it on and off again',
        'Go with the flow...',
    ]
    await ctx.send(f'Q: {question}\nA: {random.choice(responses)}')

@client.command()
async def cryptoMelba(ctx):
    CRYPTO_CHANNEL = client.get_channel(int(CRYPTO_C))
    await CRYPTO_CHANNEL.send('cryptos are on the rise mijo')

@client.command()
async def cleanupMelba(ctx, amount=10):
    await ctx.channel.purge(limit=amount)

client.run(USER)
