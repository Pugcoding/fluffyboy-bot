import discord
from discord.ext import commands
import asyncio
"""
Let users assign themselves roles by clicking on Buttons.
The view made is persistent, so it will work even when the bot restarts.
See this example for more information about persistent views:
https://github.com/Pycord-Development/pycord/blob/master/examples/views/persistent.py
Make sure to load this cog when your bot starts!
"""

# This is the list of role IDs that will be added as buttons.



class SelectMenu(discord.ui.Select):
    # This is the select menu that will be used to select the handle the question 

    def __init__(self, bot,ctx):
        super().__init__(
            custom_id="question",
        )
        self.bot = bot
        self.ctx = ctx
        self.options = [
            discord.SelectOption(label="Accept", value="accept"),
            discord.SelectOption(label="Deny", value="deny"),
            discord.SelectOption(label="Publish", value="publish"),

        ]
    
    async def callback(self, interaction: discord.Interaction):
        chosen = self.values[0]
        oldEmbed = interaction.message.embeds[0]

        if chosen == "accept":
            await interaction.response.send_message("You Have Two Minutes To Respond !", ephemeral=True)
            try:
                def check_accept(message):
                    # make sure the person who hit the button is the same person who is responding and its in the eval channel
                    return message.author == self.ctx.author and message.channel.id == 1063607720583901274
                message = await self.bot.wait_for('message', timeout=120.0, check=check_accept)
                await interaction.response.send_message("You Have Accepted The Question !", ephemeral=True)
                # get user who sent the message
                user = message.author
                # send them a dm
                await user.send("Your Question Has Been Accepted !: " + message.content)
                await interaction.response.send_message("The User Has Been Notified !", ephemeral=True)


            except asyncio.TimeoutError:
                await interaction.response.send_message("You Took Too Long To Respond !", ephemeral=True)

        elif chosen == "deny":
            await interaction.response.send_message("You Have Denied The Question !", ephemeral=True)
        elif chosen == "publish":
            await interaction.response.send_message("You Have Two Minutes To Repond!", ephemeral=True)
            try:
                #give the user two minutes to respond
                oldEmbed = interaction.message.embeds[0]

                def check(message):
                    # make sure the person who hit the button is the same person who is responding and its in the eval channel
                    return message.author.id == self.ctx.author.id and message.channel.id == 1063607720583901274
                
                message = await self.bot.wait_for('message', timeout=120.0, check=check)
    
                # get faq channel
                faq_channel = 1063400334468325416
                # get the channel
                channel = self.bot.get_channel(faq_channel)
                # make the embed
                oldEmbed.add_field(name="Answer", value=message.content, inline=False)
                # send the message with the view
                #remove the "select an option" footer
                oldEmbed.set_footer(text="")
                
                await channel.send(embed=oldEmbed)
                

            except asyncio.TimeoutError:
                await interaction.response.send_message("You Took Too Long To Respond !", ephemeral=True)
            
    

    

class ButtonSelectCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #custom_id
        self.custom_id = "question"

    
    @commands.slash_command(guild_id=1066139205060804679)
    async def question(self, ctx: discord.ApplicationContext, question:discord.Option(str)): # type: ignore
        view = discord.ui.View(timeout=None)
        view.add_item(SelectMenu(bot=self.bot,ctx=ctx))
        eval_channel = 1063607720583901274
        #get the channel
        channel = self.bot.get_channel(eval_channel)
        #make the embed
        member = ctx.author
        member_pfp = member.avatar
        embed = discord.Embed(title="Question", description=question, color=0x00ff00)
        embed.set_author(name=ctx.author.name, icon_url=member_pfp)
        embed.set_footer(text="Select an option")
        #send the message with the view
        await channel.send(embed=embed, view=view)
        await ctx.respond("Question sent!")

        

   

    @commands.Cog.listener()
    async def on_ready(self):
        """
        This method is called every time the bot restarts.
        If a view was already created before (with the same custom IDs for buttons),
        it will be loaded and the bot will start watching for button clicks again.
        """
        # This is finally the part where we load the view.
        
        view = discord.ui.View(timeout=None)
        guild = self.bot.get_guild(1063291660496293928)
        view.add_item(SelectMenu(bot=self.bot,ctx=guild))
        
        self.bot.add_view(view)
        



def setup(bot):
    bot.add_cog(ButtonSelectCog(bot))

