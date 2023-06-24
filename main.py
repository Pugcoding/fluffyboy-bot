import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import math
import textwrap
import discord
from discord import Webhook
import requests
from dotenv import load_dotenv
from discord import Emoji
import random
import tweepy
from discord.ext import commands
from better_profanity import profanity
import json
from threading import Thread
import asyncio
import yt_dlp as youtube_dl
import redditeasy
import aiohttp
from googletrans import Translator
import re

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

fanart_channels = [server_channels["\u2b1bralsei-art"], server_channels["utdr-art"], server_channels["general-art"]]
# YT Config


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
                  "lookdown_blush", "sad", "sad_blush", "sad_fangs", "ser", "stare","pirate"]

# Thanks to Tom for the Pirate Ralsei Sprite!

"""
-Pug April 18th 2023 
I Like Leaving little notes like this :3


"""

    

# API Keys
global twitter_client
twitter_client = tweepy.Client(str(os.getenv('TWEEPY')))



async def say(text, sprite, ctx):
    text, sprite = text.lower(), sprite.lower() # make sure everything is lowercase
    if sprite not in ralsei_sprites: # check if sprite is valid
        await ctx.respond("Invalid sprite!", ephemeral=True) # if not, send error message
    elif profanity.contains_profanity(text): # check if text contains profanity
        await ctx.respond("No swearing!", ephemeral=True) # if so, send error message
    elif len(text) > 72: # check if text is too long
        await ctx.respond("Text too long!", ephemeral=True) # if so, send error message
    else:
        img_text = '\n'.join(textwrap.wrap(text, 26)) # wrap text

        im = Image.open(f"ralsei_faces/{sprite}.png") # open image
        fnt = ImageFont.truetype("DTM-Mono.otf", 24) # load font and size
        d = ImageDraw.Draw(im) # draw image
        d.multiline_text((160, 40), img_text, font=fnt, fill="#ffffff") # draw text
        filename = f"result.png" # set filename
        im.save(filename)    # save image
        await ctx.respond(file=discord.File(open(filename, "rb"))) # send image
"""
@bot.slash_command(name='bugreport',description='report a bug')
async def bugreport(ctx):
    await ctx.send_modal(BugReportForm(title="Bug Report"))
"""

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Ralsei Hugging Simulator " + str(datetime.now().year))) # sets to fake game
    
@bot.slash_command(name="echo", description="Echoes your message ")
@commands.has_permissions(manage_messages=True)
async def echo(ctx, message: str, channel: discord.TextChannel = None):
    """
    Allows you to send messages as the bot
    """
    no_channel_selected = bool(channel == None)
    if no_channel_selected:
        await ctx.respond("please specify a channel", ephemeral=True)
    await channel.send(message)
    await ctx.respond("Message sent", ephemeral=True)




@bot.event
async def on_message(message):
    message_is_from_bot = bool(message.author == bot.user)
    if message_is_from_bot:  # Prevents bot from responding to itself
        return
    if "boykisser" in message.content.lower() or "kissing boys" in message.content.lower():
        roll = random.randint(1, 20)
        if roll == 1:
            await message.channel.send("oohh you like kissing boys dont you...")
            # change name to boykisser
            await message.author.edit(nick=(message.author.name + " ( boykisser)"))


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

@bot.slash_command(name="block", description="Block a user from using you in interaction commands")
async def block(ctx, user: discord.Option(discord.User, description="The user you want to block")):
    """
    Blocks a user from using the bot in interaction commands.

    Args:
        ctx (discord.InteractionContext): The context of the interaction.
        user (discord.User): The user to be blocked.

    Returns:
        None
    """
    with open("blacklist.json", "r") as f:
        blocked = json.load(f)
        if str(ctx.author.id) not in blocked:
            blocked[str(ctx.author.id)] = {}
            blocked[str(ctx.author.id)]["blocked"] = {}
            blocked[str(ctx.author.id)]["blocked"][str(user.id)] = "true"
            with open("blacklist.json", "w") as f:
                json.dump(blocked, f)
                await ctx.respond("User has been blocked from using you in interaction commands")
        else:
            blocked[str(ctx.author.id)]["blocked"][str(user.id)] = "true"
            with open("blacklist.json", "w") as f:
                json.dump(blocked, f)
                await ctx.respond("User has been blocked from using you in interaction commands")

async def check_if_blocked(ctx, user, author):
    with open("blacklist.json", "r") as f:
        blocked = json.load(f)
    if str(user.id) in blocked and blocked[str(user.id)]["blocked"].get(str(author.id), "false") == "true":
        ctx.respond("You have been blocked from using this command by the user")
        return True
    
            


@bot.slash_command(name="unblock", description="Unblock a user from using you in interaction commands")
async def unblock(ctx, user: discord.Option(discord.User, description="The user you want to unblock")):
    with open("blacklist.json", "r") as f:
        blocked = json.load(f)
        if str(ctx.author.id) not in blocked:
            await ctx.respond("You have not blocked anyone")
        else:
            blocked[str(ctx.author.id)]["blocked"][str(user.id)] = "false"
            with open("blacklist.json", "w") as f:
                json.dump(blocked, f)
                await ctx.respond("User has been unblocked from using you in interaction commands")
@bot.slash_command()
async def ralsay_options(ctx):
    await ctx.respond(
        "for the sprite option, you can choose from: angry, classic, happy, light_blush, light_classic, light_happy, "
        "lookdown, lookdown_blush, sad, sad_blush, sad_fangs, ser, stare",
        ephemeral=True)


@bot.slash_command(name="ralsay", description="Make Ralsei Say Something!")
async def ralsei(ctx, text: discord.Option(str), sprite: discord.Option(str)):
    await say(text, sprite, ctx)


@bot.slash_command(name='ralsay_classic', description='V1 of the ralsay command')
async def ralsay_classic(ctx, text: discord.Option(str)):
    await say(text, 'classic', ctx)





# dance command
@bot.slash_command(name="dance", description="Dance with Ralsei!")
async def dance(ctx):
    await ctx.respond(f"{ctx.author.mention} is dancing!")
    


@bot.slash_command(name="kiss", description="Give someone a kiss!")
@commands.cooldown(1, 25, commands.BucketType.user)
async def kiss(ctx, user: discord.Option(discord.Member)):
    if await check_if_blocked(ctx, user, ctx.author):
        return
    await ctx.respond(f"{ctx.author.mention} gave {user.mention} a kiss!")
    roll = random.randint(1, 10)
    # username change chance
    if roll == 1:
        # boykisser username change
        await ctx.send("Ohh you like kissing boys")
        await ctx.author.edit(nick=(ctx.author.name + " (boykisser)"))
        await user.edit(nick=(user.name + " (boykisser)"))
    if "boykisser" in ctx.author.name:
        await ctx.author.edit(nick=(ctx.author.name + " (MEGA boykisser)"))
    if "boykisser" in user.name:
        await user.edit(nick=(user.name + " (ULTRA boykisser)"))


@kiss.error
async def kiss_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        roll = random.randint(1, 20)
        if roll == 1:
            await ctx.respond(f"Slow down! You can kiss someone again in {error.retry_after:.2f} seconds.",
                              ephemeral=True)
        else:
            # username change chance
            await ctx.respond("You just cant wait to kiss someone again, can you?")
            await ctx.author.edit(nick=(ctx.author.name + " (boykisser)"))



# stab command
@bot.slash_command(name="stab", description="Stab someone!")
@commands.cooldown(1, 10, commands.BucketType.user)
async def stab(ctx, user: discord.Option(discord.Member)):
    if await check_if_blocked(ctx, user, ctx.author):
        return
    await ctx.respond(f"{ctx.author.mention} stabbed {user.mention}!")

    roll = random.randint(1, 10)
    if roll == 1:
        await ctx.send("oh no")
    if roll == 2:
        await ctx.send("you gotta a license for that?")
    if roll == 3:
        await ctx.send("why would you do that?")
    

@stab.error
async def stab_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        roll = random.randint(1, 2)
        if roll == 1:
            await ctx.respond(f"Slow down! You can stab someone again in {error.retry_after:.2f} seconds.",
                              ephemeral=True)
        else:
            # username change chance
            await ctx.respond("You just cant wait to stab someone again, can you?")
            await ctx.author.edit(nick=(ctx.author.name + " (stabber)"))

#clear command
@bot.slash_command(name="clear", description="Clear a certain amount of bot messages!")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: discord.Option(int)):
    #only clear bot messages
    def is_bot(m):
        return m.author == bot.user
    await ctx.channel.purge(limit=amount, check=is_bot)
    await ctx.respond(f"{amount} messages have been cleared!", ephemeral=True)



# cuddle command
@bot.slash_command(name="cuddle", description="Cuddle with someone!")
@commands.cooldown(1, 10, commands.BucketType.user)
async def cuddle(ctx, user: discord.Option(discord.Member)):
    if await check_if_blocked(ctx, user, ctx.author):
        return
    
    await ctx.respond(f"{ctx.author.mention} cuddled {user.mention}!")
    roll = random.randint(1, 10)
    if roll == 1:
        await ctx.send("aww")
    if roll == 2:
        await ctx.send("cute")
    if roll == 3:
        await ctx.send("cuddles are nice!")
    if roll == 4:
        await ctx.send("cuddles are the best!")


@cuddle.error
async def cuddle_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(f"Slow down! You can cuddle someone again in {error.retry_after:.2f} seconds.",
                          ephemeral=True)
    roll = random.randint(1, 2)
    if roll == 1:
        await ctx.author.edit(nick=(ctx.author.name + " (cuddler)"))


people_would_you_rather = ["Chara","Sans","Ralsei","Noelle","Susie","Toriel","Spamton","Lancer","Berdly"]

would_you_rather_sen = ["Be stuck in a room with","Be bullied by","Have to fight","Have dinner with","Cuddle with" ]



    


# hug command

# add cooldown
@bot.slash_command(name="hug", description="Give someone a hug!")
@commands.cooldown(1, 10, commands.BucketType.user)
async def hug(ctx, user: discord.Option(discord.Member)):
    await ctx.respond(f"{ctx.author.mention} gave {user.mention} a hug!")
    roll = random.randint(1, 10)
    if roll == 1:
        await ctx.send("aww")
    if roll == 2:
        await ctx.send("cute")
    if roll == 3:
        await ctx.send("hugs are nice!")


@hug.error
async def hug_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(f"Slow down! You can hug someone again in {error.retry_after:.2f} seconds.",
                          ephemeral=True)


# cookie command
@bot.slash_command(name="cookie", description="Give someone a cookie!")
@commands.cooldown(1, 10, commands.BucketType.user)
async def cookie(ctx, user: discord.Option(discord.Member)):
    await ctx.respond(f"{ctx.author.mention} gave {user.mention} a cookie!")
    roll = random.randint(1, 5)
    if roll == 1:
        await ctx.send("yum yum yum")


@cookie.error
async def cookie_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(f"Slow down! You can give someone a cookie again in {error.retry_after:.2f} seconds.",
                          ephemeral=True)


# group hug command

@bot.slash_command(name="boop", desription="boop someone!")
@commands.cooldown(1, 10, commands.BucketType.user)
async def boop(ctx, user: discord.Option(discord.Member)):
    await ctx.respond(f"{ctx.author.mention} booped {user.mention}!")
    

@boop.error
async def boop_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(f"Slow down! You can boop someone again in {error.retry_after:.2f} seconds.",
                          ephemeral=True)

@bot.slash_command(name="group_hug", description="Give everyone a hug!")
@commands.cooldown(1, 10, commands.BucketType.user)
async def group_hug(ctx):
    await ctx.respond(f"{ctx.author.mention} gave everyone a hug!")
    roll = random.randint(1, 5)
    if roll == 1:
        await ctx.send("aww")
    if roll == 2:
        await ctx.send("cute")
    if roll == 3:
        await ctx.send("hugs are nice!")


@group_hug.error
async def group_hug_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(f"Slow down! You can hug everyone again in {error.retry_after:.2f} seconds.",
                          ephemeral=True)


# kill command

@bot.slash_command(name="kill", description="how dare you!")
@commands.cooldown(1, 10, commands.BucketType.user)
async def kill(ctx, user: discord.Option(discord.Member)):
    await ctx.respond(f"{ctx.author.mention} killed {user.mention}!")
    roll = random.randint(1, 5)
    roll_two = random.randint(1, 20)
    if roll == 1:
        await ctx.send("you monster!")
    if roll_two == 1:
        await ctx.send(
            'Im killing you. Im killing you. I dont care about anything else, I dont give a shit about anything else, I- My programming is just "GET THAT FUCKING GUY RIGHT NOW"')


@kill.error
async def kill_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(f"Slow down! You can KILL everyone again in {error.retry_after:.2f} seconds.",
                          ephemeral=True)
        

@bot.slash_command(name='pet',description='pet somebody')
@commands.cooldown(1,10, commands.BucketType.user)
async def pet(ctx,member: discord.Option(discord.Member)):
    message_options =[f"{ctx.author.mention} pet {member.mention}",f"{ctx.author.mention} gave {member.mention} headpats",f"{member.mention} was pet by {ctx.author.mention}"]
    await ctx.respond(random.choice(message_options))
    
    


# Need to implement pinheads cog loader

bot.load_extension('cogs.roles')
bot.load_extension('cogs.roles_two')
bot.load_extension('cogs.roles_three')
bot.load_extension('cogs.roles_four')

bot.run(TOKEN)

"""
code ran past this point will not be run


"""









