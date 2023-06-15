import discord
from discord.ext import commands
import random
import asyncio



class admin_commands(commands.Cog):




    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def emoji_debug(self, ctx, emoji: discord.Emoji):
        await ctx.respond(f"Emoji name: {emoji.name}\nEmoji ID: {emoji.id}\nEmoji URL: {emoji.url}", ephemeral=True)

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason):

        ban_msg_random = ["has been banned", "hit the ground to hard", "has been terminated", "didnt juju on that beat",
                          "has been eliminated", "didnt have uno on his xbox", "took too many melatonin gummies"]
        
        # ban user
        ctx.guild.ban(member, reason=reason)
        # send message
        await ctx.respond(f"{member.name} {random.choice(ban_msg_random)}")
        









def setup(bot):
    bot.add_cog(admin_commands())
