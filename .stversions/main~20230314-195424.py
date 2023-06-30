import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import math
import textwrap
import discord
import requests
from dotenv import load_dotenv
from discord import Emoji
import time
import ffmpeg
import random
import tweepy
from discord.ext import commands
import psutil
import subprocess
from better_profanity import profanity
import threading
import json
from threading import Thread
import asyncio
import yt_dlp as youtube_dl
load_dotenv()


# Bot Startup
TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = str(TOKEN)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = discord.Bot(intents=intents)



# Load Channel Directory
with open('channel.json', 'r') as openfile:

    # Reading from json file
    server_channels = json.load(openfile)


# YT Config

youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


# Important Values       
global logging_channel

channelid = bot.get_channel("channel id")

logging_channel = channelid
other_intro = 1063452510708310066

last_author = "Pug"

yes_emoji = (1064813330541322250)

no_emoji = (1064813350548164670)

star_emoji = (1063628977027158048)

ralsei_sprites = ["angry", "classic", "happy", "light_blush", "light_classic", "light_happy", "lookdown",
                  "lookdown_blush", "sad", "sad_blush", "sad_fangs", "ser", "stare"]

# API Keys
global twitter_client
twitter_client = tweepy.Client(
    "AAAAAAAAAAAAAAAAAAAAAJzelQEAAAAAr25TLueVifcE9swjWk0wkrsxetQ%3DBu19hboo1T16Gy9dPbpmWSZV2jEqbFN4JEyp98k3E2YZjyQvcE")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='3cc5a524427a45459f7866b772ba9959',
                                               client_secret='cc648381c30744b09e8dfc320ec926b9',
                                               redirect_uri='http://localhost:8888/callback',
                                               scope='user-library-read,user-modify-playback-state'))


# Functions and Checks

def json_check(file, key):
    try:
        with open(f"{file}.json", "r") as f:
            reactions = json.load(f)
            return list(reactions[key])
    except FileNotFoundError:
        print("File Not Found, Make sure you only have the file name and not the extension! ")
    except KeyError:
        print("Key Not Found, Make sure you only have the key name!")

async def yes_no(message): 
    await message.add_reaction(bot.get_emoji(yes_emoji))
    await message.add_reaction(bot.get_emoji(no_emoji))


async def star(message):
    await message.add_reaction(bot.get_emoji(star_emoji))




async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

async def play_song(ctx,url):
    server = bot.get_guild(ctx.guild.id)
    voice_channel = server.voice_client
    await ctx.send("Playing " + await get_title(url))
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop)
        voice_channel.play(discord.FFmpegPCMAudio(player))


async def leave(ctx):
    voice_client = bot.get_guild(ctx.guild.id)
    await voice_client.disconnect()

async def stop(ctx):
    voice_client = bot.get_guild(ctx.guild.id)
    voice_client.stop()

async def pause(ctx):
    voice_client = bot.get_guild(ctx.guild.id)
    voice_client.pause()

async def resume(ctx):
    voice_client = bot.get_guild(ctx.guild.id)
    voice_client.resume()

async def leave(ctx):
    voice_client = bot.get_guild(ctx.guild.id)
    await voice_client.disconnect()

async def say(text, sprite, ctx):
    text, sprite = text.lower(), sprite.lower()
    if sprite not in ralsei_sprites:
        await ctx.respond("Invalid sprite!", ephemeral=True)
    elif profanity.contains_profanity(text):
        await ctx.respond("No swearing!", ephemeral=True)
    elif len(text) > 72:
        await ctx.respond("Text too long!", ephemeral=True)
    else:
        img_text = '\n'.join(textwrap.wrap(text, 26))

        im = Image.open(f"ralsei_faces/{sprite}.png")
        fnt = ImageFont.truetype("DTM-Mono.otf", 24)
        d = ImageDraw.Draw(im)
        d.multiline_text((160, 40), img_text, font=fnt, fill="#ffffff")
        filename = f"result.png"
        im.save(filename)
        await ctx.respond(file=discord.File(open(filename, "rb")))

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Ralsei Hugging Simulator " + str(datetime.now().year)))









@bot.slash_command(name="join", description="Joins the voice channel you are in")
async def _join(ctx):
    await join(ctx)

@bot.slash_command(name="play", description="Plays a song from youtube")
async def _play(ctx, url: str):
    await play_song(ctx,url)

@bot.slash_command(name="leave", description="Leaves the voice channel")
async def _leave(ctx):
    await leave(ctx)

@bot.slash_command(name="stop", description="Stops the song")
async def _stop(ctx):
    await stop(ctx)

@bot.slash_command(name="pause", description="Pauses the song")
async def _pause(ctx):
    await pause(ctx)

@bot.slash_command(name="resume", description="Resumes the song")
async def _resume(ctx):
    await resume(ctx)

@bot.slash_command(name="leave", description="Leaves the voice channel")
async def _leave(ctx):
    await leave(ctx)







fanart_channels = [server_channels["ralsei-fanart"], server_channels["utdr-art"], server_channels["general-art"]]







@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id in json_check("reaction", "suggest"):
        await yes_no(message)
    if message.channel.id in json_check("reaction", "fanart"):
        if message.attachments:
            await star(message)
    # question channel test

    if message.channel.id == 1063627336941060106:
        if message.reference is not None:
                bot.get_message(message.reference.message_id)
                await message.add_reaction("✅")
                await message.channel.send(message.reference.content)


    # caption reminder
    if message.channel.id == int(server_channels["ralsei-fanart"]):
        if not message.attachments:
            if "caption" not in message.content.lower():
                await message.delete()
                await message.channel.send(
                    ' Please use "Caption:" at the front of your message if you want to add a caption to your art. If you are not posting art and just want to talk about art sent in this channel, use 🟢║ralsei-discussion and mention the artist that posted the art! Thank you!',
                    delete_after=30)
    if message.channel.id == int(server_channels["general-art"]):
        if not message.attachments:
            if "caption" not in message.content.lower():
                await message.delete()
                await message.channel.send(
                    'Please use "Caption:" at the front of your message if you want to add a caption to your art. If you are not posting art and just want to talk about art sent in this channel, use 👥║general-discussion  and mention the artist that posted the art! Thank you!',
                    delete_after=30)


# paste here
# Role_Two Collection
@bot.event
async def on_member_ban():
    invites = await member.guild.invites()
    for invite in invites:
        if invite.inviter == member:
            await invite.delete()


@bot.slash_command(name="angel", description="Get information about angel aka. dailyralsei")
async def angel(ctx):
    embed = discord.Embed(
        title='Information about DailyRalsei',
        description="Here's some information about DailyRalsei",
        colour=discord.Colour.green()

    )
    embed.set_author(name="DailyRalsei",
                     icon_url="https://pbs.twimg.com/profile_images/1612237599900598278/sF--GKor_400x400.png")
    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1612237599900598278/sF--GKor_400x400.png")
    embed.add_field(name="Twitter", value="https://twitter.com/ralseihugs", inline=False)
    embed.add_field(name="Ko-Fi", value="https://t.co/9hqF2QXWUN", inline=False)
    await ctx.respond(embed=embed)  # Send the embed with some text


@bot.slash_command(name="deltarune", description="Get information about Deltarune")
async def deltarune(ctx):
    embed = discord.Embed(
        title='Information about Deltarune',
        description="Here's some information about Deltarune",
        colour=discord.Colour.green()
    )
    embed.set_thumbnail(
        url="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fattackofthefanboy.com%2Fwp-content%2Fuploads%2F2018%2F11%2Fdeltarune-logo.png&f=1&nofb=1&ipt=379230a8f35e0059a2bc4a61282a8b4c78189db2a741047e10b8ed47e1f3d8d1&ipo=images")
    embed.add_field(name="Developer", value="Toby Fox", inline=False)
    embed.add_field(name="Release Date", value="October 31st, 2018", inline=False)
    embed.add_field(name="Genre", value="RPG", inline=False)
    embed.add_field(name="Platforms", value="Windows, Mac, Linux, Nintendo Switch", inline=False)
    embed.add_field(name="Website", value="https://deltarune.com/", inline=False)
    await ctx.respond(embed=embed)  # Send the embed with some text


@bot.slash_command(name="newest_tweet", description="Get the newest tweet from DailyRalsei")
async def newest_tweet(ctx):
    ralsei_id = 1545991798593490944
    response = twitter_client.get_users_tweets(ralsei_id, max_results=5)
    for tweet in response.data:
        if "RT @" in tweet.text:
            pass
        else:
            tweet.id = str(tweet.id)
            await ctx.respond(
                "The Newest Tweet From Daily Ralsei: " + "https://twitter.com/ralseihugs/status/" + tweet.id)
            break


@bot.slash_command()
async def ralsay_options(ctx):
    await ctx.respond(
        "for the sprite option, you can choose from: angry, classic, happy, light_blush, light_classic, light_happy, lookdown, lookdown_blush, sad, sad_blush, sad_fangs, ser, stare",
        ephemeral=True)


@bot.slash_command(name="ralsay", description="Make Ralsei Say Something!")
async def ralsei(ctx, text: discord.Option(str), sprite: discord.Option(str)):
    await say(text, sprite, ctx)




bot.load_extension('cogs.roles')
bot.load_extension('cogs.roles_two')
bot.run(TOKEN)

# test
