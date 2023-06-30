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
TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = str(TOKEN)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = discord.Bot(intents=intents)

global logging_channel

channelid = bot.get_channel("channel id")

logging_channel = channelid
other_intro = 1063452510708310066


def json_check(file, key):
    try:
        with open(f"{file}.json", "r") as f:
            reactions = json.load(f)
            return list(reactions[key])
    except FileNotFoundError:
        print("File Not Found, Make sure you only have the file name and not the extension! ")
    except KeyError:
        print("Key Not Found, Make sure you only have the key name!")


# API Keys
global twitter_client
twitter_client = tweepy.Client(
    "AAAAAAAAAAAAAAAAAAAAAJzelQEAAAAAr25TLueVifcE9swjWk0wkrsxetQ%3DBu19hboo1T16Gy9dPbpmWSZV2jEqbFN4JEyp98k3E2YZjyQvcE")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Ralsei Hugging Simulator " + str(datetime.now().year)))


last_author = "Pug"

yes_emoji = (1064813330541322250)

no_emoji = (1064813350548164670)

star_emoji = (1063628977027158048)

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



async def yes_no(message):
    emoji = bot.get_emoji(yes_emoji)
    await message.add_reaction(emoji)
    emoji = bot.get_emoji(no_emoji)
    await message.add_reaction(emoji)


async def star(message):
    emoji = bot.get_emoji(star_emoji)
    await message.add_reaction(emoji)

async def get_title(url):
    r = requests.get(url)
    title = r.text.split('<title>')[1].split('</title>')[0].split(' - YouTube')[0]
    return title


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


ralsei_sprites = ["angry", "classic", "happy", "light_blush", "light_classic", "light_happy", "lookdown",
                  "lookdown_blush", "sad", "sad_blush", "sad_fangs", "ser", "stare"]


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


server_channels = {
    "check-rank": 1063449011060756531,
    "find-my-ralsei": 1063364711460118589,
    "defender-jrs": 1063410598651641907,
    "plush-board": 1070178558196060171,
    "the-daily-plush": 1063446685461782588,
    "general": 1063418479933403146,
    "comic-art-teasers": 1064692233955201064,
    "ralsei-positivity-media": 1067576016542892144,
    "sillier-chill": 1067578993479524402,
    "ralsei-positivity": 1067575179414360084,
    "self-promo": 1064334763009253486,
    "the prince's room": 1063849809452204155,
    "tasque-manager": 1063612837211164692,
    "general-discussion": 1063357803894419497,
    "read this, silly": 1063350241560121384,
    "the cauldron": 1063291661276426311,
    "rude-buster": 1063395990389927957,
    "staff-intros": 1063452510708310066,
    "emote-suggest": 1063420126696845363,
    "ralsei-discussion": 1063637463752511518,
    "Comic Team Chat": 1064319392193724447,
    "plush-game": 1070177343844388864,
    "comic-announcements": 1066147979771256842,
    "Town Square": 1063483219321835582,
    "plush palace": 1070131044050796574,
    "utdr-memes": 1063363604285505556,
    "Comic Town!": 1064258742473986088,
    "greetings": 1063291661276426313,
    "utdr-art": 1063367929426616351,
    "events-no-mic": 1070179688133177475,
    "starbe-comics": 1069309243263557653,
    "art-progress": 1064264489727426612,
    "storyboarding": 1064264505036644443,
    "plush-suggestions": 1070180100991090790,
    "silly-intros": 1063370114830962730,
    "no-mic": 1063434380019761153,
    "music-bot-commands": 1063482843050803281,
    "silent-room": 1063624322838712441,
    "defenders": 1063358685608419339,
    "deltarune au comic": 1066135457995440168,
    "music-progress": 1064264478717382786,
    "yggdrasil": 1064144949425213460,
    "Peaceful Bench": 1063483374292963328,
    "food-stuff": 1069892715719970846,
    "ralsei-memes": 1063364269699252294,
    "Jukebox": 1063483870055510056,
    "Talkin N’ Chatter": 1063291661276426312,
    "moderation-log": 1064253824417681448,
    "pets-and-goobers": 1067083950222225519,
    "work-organization": 1064324440311222352,
    "rules": 1070178464646320168,
    "server-events": 1063641148972879883,
    "owo": 1063477769822011484,
    "emote-idea-dump": 1063745084719382568,
    "uh-oh": 1063358714070974484,
    "the void": 1067420408615284767,
    "rales": 1063541476153364491,
    "test": 1063360437153976340,
    "ralsei-says": 1070121963600752640,
    "discussion-media": 1063852435623395389,
    "general-art": 1063366734100320296,
    "mysterious closet": 1066130929237631026,
    "daily-ralsei": 1063641344817496105,
    "angle's corner": 1063643710237192272,
    "team-general": 1064264444387020860,
    "game-vc-chat": 1066127414666735636,
    "suggestions": 1065848129695535184,
    "suggestions-discussion": 1067018389693923348,
    "School Closet": 1063483481012838451,
    "ralsei-fanart": 1063366669940031508,
    "Castle Town": 1063291661276426314,
    "bot-spam": 1063449651895873617,
    "mailbox": 1066131790235967668,
    "utdr-discussion": 1063356125895995423,
    "announcements": 1064255651179667517,
    "roles": 1063350606024146984,
    "Cyber City": 1063448784216002620,
    "general-memes": 1063363632613834772,
    "eval": 1063607720583901274,
    "tasque-os": 1063397293212053534,
    "castletown": 1063358633091547148,
    "carl": 1064150077884612658,
    "ask-a-question": 1063605582654873700,
    "owo-game-angle": 1063642959100252200,
    "rules": 1063349548975661126,
    "dealer-stash": 1063292781709230201,
    "bot-spam": 1063644757521338448,
    "frequently-asked": 1063400334468325416,

}

fanart_channels = [server_channels["ralsei-fanart"], server_channels["utdr-art"], server_channels["general-art"]]


def check(message):
    return message.author == interaction.user
def question(og_message, anwser):
    # Publish a message
    class question(discord.ui.View):  # Create a class called MyView that subclasses discord.ui.View
        @discord.ui.button(label="Accept",
                           style=discord.ButtonStyle.green)  # Create a button with the label "😎 Click me!" with color Blurple
        async def button_accept(self, button, interaction):
            await interaction.response.send_message(
                "Interaction Placeholder")  # Send a message when the button is clicked

        @discord.ui.button(label="Decline",
                           style=discord.ButtonStyle.danger)  # Create a button with the label "😎 Click me!" with color Blurple
        async def button_decline(self, button, interaction):
            await interaction.response.send_message(
                "Interaction Placeholder")  # Send a message when the button is clicked

        @discord.ui.button(label="Publish",
                           style=discord.ButtonStyle.primary)  # Create a button with the label "😎 Click me!" with color Blurple
        async def button_publish(self, button, interaction):
            await interaction.response.send_message(
                "You have one Minute to answer the question")  # Send a message when the button is clicked
            try:
                msg = await bot.wait_for("message", timeout=60)

            except asyncio.TimeoutError:
                await msg.channel.send("You took too long to answer")


def publish(msg):
    embed = discord.Embed(title="FAQ", description="A new fanart has been published!", color=0x00ff00)





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
