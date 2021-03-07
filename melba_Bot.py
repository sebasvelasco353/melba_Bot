import os
import random
import discord
import requests
import youtube_dl
from discord.ext import commands

USER = os.getenv('MELBA_BOT')
CRYPTO_C = os.getenv('CRYPTO_CHANNEL')
client = commands.Bot(command_prefix = '!')

# Helper function to know if the bot its already on the voice channel
def is_connected(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice:
        return True
    else:
        return False


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


@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='Just chillin')
    if not is_connected(ctx):
        await voiceChannel.connect()

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Finished playing song"))

@client.command()
async def leave(ctx):
       voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
       if voice.is_connected():
           await voice.disconnect()
       else:
           await ctx.send("Melba isnt in the server mijo.")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("nothing playing mijo")

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused:
        voice.resume()
    else:
        await ctx.send("The audio is not paused")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

client.run(USER)
