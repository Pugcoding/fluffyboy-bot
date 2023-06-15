import discord
from discord.ext import commands, tasks
import random
import os
import asyncio

items = {
    "Dark Candy": {
        "description": "Heals 40 HP",
        "hp": 40,
        "use_message": "Dark Candy was used. It's Burnt."

    },
    "Darkburger": {
        "description": "Heals 70 HP",
        "hp": 70,
        "use_message": "Darkburger was used. It's Burnt."
    },
    "Choco Diamond": {
        "description": "Heals 60 HP",
        "hp": 60,
        "use_message": "Choco Diamond was used. mmm chocolatey."
    },
    "Lancer Cookie": {
        "description": "Heals 50 HP",
        "hp": 50,
        "use_message": "Lancer Cookie was used. You feel strange."
    },
    "CD Bagel": {
        "description": "Heals 80 HP",
        "hp": 80,
        "use_message": "CD Bagel was used. You feel a little more energized."
    },
    "Java Cookie": {
        "description": "Heals 90 HP",
        "hp": 90,
        "use_message": "Java Cookie was used. You feel a little more energized."
    },
    "Kris Tea": {
        "description": "Heals 100 HP",
        "hp": 100,
        "use_message": "Kris Tea was used. You feel a little stronger."
    },
    "Susie Tea": {
        "description": "Heals 100 HP",
        "hp": 100,
        "use_message": "Susie Tea was used. You feel more aggressive."
    },
    "Ralsei Tea": {
        "description": "Heals 100 HP",
        "hp": 100,
        "use_message": "Ralsei Tea was used. You feel a sense of calmness."
    },
    "Noelle Tea": {
        "description": "Heals 100 HP",
        "hp": 100,
        "use_message": "Noelle Tea was used. You feel a little better."
    },
    "Berdly Tea": {
        "description": "Heals -20 HP",
        "hp": -20,
        "use_message": "Berdly Tea was used. The taste was so bad that it actually hurt you."
    },

}


class minigame_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="challenge")
    @commands.has_permissions(administrator=True)
    async def challenge(self, ctx, user: discord.User):
        await ctx.respond(
            f"{user.mention}, {ctx.author.mention} has challenged you to a deltarune minigame! Do you accept? (yes/no)")

        def check(m):
            return m.author == user and m.channel == ctx.channel

        try:
            # Wait for the author to respond with yes or no
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            # If we hit a timeout, say goodbye
            await ctx.respond(f"{user.mention} didn't respond in time... :(")
            return
        else:

            # If we got a message, cancel the task and respond
            if msg.content.lower() == "yes":
                await ctx.respond(f"{user.mention} has accepted the challenge!")
                # create a thread for the minigame
                thread_name = f"{ctx.author.name} vs {user.name}"
                # get current channel
                channel = ctx.channel
                # create the thread
                await channel.create_thread(name=thread_name, auto_archive_duration=1440, reason="Minigame")
                # get the thread
                thread = discord.utils.get(ctx.guild.threads, name=thread_name)
                # send message with link to thread
                await ctx.respond(f"Click [here]({thread}) to go to the thread!")
                # set up the minigame
                player1 = ctx.author
                player2 = user
                player1_hp = 100
                player2_hp = 100
                player1_items = []
                player2_items = []
                # pick 3 random items for each player
                for i in range(3):
                    player1_items.append(random.choice(list(items.keys())))
                    player2_items.append(random.choice(list(items.keys())))

                while True:
                    # start minigame loop
                    # player 1's turn
                    if player1_hp <= 0:
                        # player 1 loses
                        await thread.send(f"{player1.mention} has lost!")
                        break
                    elif player2_hp <= 0:
                        # player 2 loses
                        await thread.send(f"{player2.mention} has lost!")
                        break
                    else:
                        # send HP
                        await thread.send(f"{player1.mention}'s HP: {player1_hp}\n{player2.mention}'s HP: {player2_hp}")
                        await thread.send(f"{player1.mention}'s turn!")
                        # send the items
                        embed = discord.Embed(title="Items", description="Pick an item to use! or Fight!", color=0x00ff00)
                        for i in range(len(player1_items)):
                            # if the item slot is empty
                            if player1_items[i] == "Empty":
                                embed.add_field(name=f"Item {i+1}", value="Empty", inline=False)
                            else:
                                embed.add_field(name=f"Item {i+1}", value=f"{player1_items[i]}: {items[player1_items[i]]['description']}", inline=False)
                        await thread.send(embed=embed)
                        # check for response
                        def check(m):
                            return m.author == player1 and m.channel == thread
                        try:
                            # Wait for the author to respond with yes or no
                            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
                        except asyncio.TimeoutError:
                            # If we hit a timeout, say goodbye
                            await thread.send(f"{player1.mention} didn't respond in time... :(")
                            break
                        else:
                            if msg.content.lower() == "fight":
                                # player 1 attacks player 2
                                damage = random.randint(10, 20)
                                player2_hp -= damage
                                await thread.send(f"{player1.mention} attacked {player2.mention} for {damage}HP !")
                                if player2_hp <= 0:
                                    # player 2 loses
                                    await thread.send(f"{player2.mention} has lost!")
                                    # end the minigame and delete the thread
                                    thread.send("The thread will be deleted in 30 seconds.")
                                    await asyncio.sleep(30)
                                    await thread.delete()

                                    break
                                else:
                                    await thread.send(f"{player2.mention} has {player2_hp}HP left!")
                            # check if the item slot is full
                            elif player1_items[int(msg.content)-1] == "Empty":
                                await thread.send("That slot is empty!")
                            else:
                                # use the item
                                player1_hp += items[player1_items[int(msg.content)-1]]["hp"]
                                await thread.send(items[player1_items[int(msg.content)-1]]["use_message"])
                                # remove the item from the list
                                player1_items[int(msg.content)-1] = "Empty"
                            if player1_items == ["Empty", "Empty", "Empty"]:
                                await thread.send("You have no more items!")
                            else:
                                await thread.send("Invalid command!")
                                await thread.send("skipping turn...")
                        # player 2's turn
                        if player1_hp <= 0:
                            # player 1 loses
                            await thread.send(f"{player1.mention} has lost!")
                            break
                        elif player2_hp <= 0:
                            # player 2 loses
                            await thread.send(f"{player2.mention} has lost!")
                            break
                        else:
                            await thread.send(f"{player2.mention}'s turn!")
                            # send the items
                            embed = discord.Embed(title="Items", description="Pick an item to use! or Fight!", color=0x00ff00)
                            for i in range(len(player2_items)):
                                # if the item slot is empty
                                if player2_items[i] == "Empty":
                                    embed.add_field(name=f"Item {i+1}", value="Empty", inline=False)
                                else:
                                    embed.add_field(name=f"Item {i+1}", value=f"{player2_items[i]}: {items[player2_items[i]]['description']}", inline=False)
                            await thread.send(embed=embed)
                            # check for response
                            def check(m):
                                return m.author == player2 and m.channel == thread
                            try:
                                # Wait for the author to respond
                                msg = await self.bot.wait_for('message', check=check, timeout=30.0)
                            except asyncio.TimeoutError:
                                await thread.send(f"{player2.mention} didn't respond in time... :(")
                                break
                            else:
                                # check if the item slot is full
                                if player2_items[int(msg.content)-1] == "Empty":
                                    await thread.send("That slot is empty!")
                                else:
                                    # use the item
                                    player2_hp += items[player2_items[int(msg.content)-1]]["hp"]
                                    await thread.send(items[player2_items[int(msg.content)-1]]["use_message"])
                                    # remove the item from the list
                                    player2_items[int(msg.content)-1] = "Empty"
                                if player2_items == ["Empty", "Empty", "Empty"]:
                                    await thread.send("You have no more items!")
                                if msg.content.lower() == "fight":
                                    # player 2 attacks player 1
                                    damage = random.randint(10, 20)
                                    player1_hp -= damage
                                    await thread.send(f"{player2.mention} attacked {player1.mention} for {damage}HP !")
                                    if player1_hp <= 0:
                                        # player 1 loses
                                        await thread.send(f"{player1.mention} has lost!")
                                        # end the minigame and delete the thread
                                        thread.send("The thread will be deleted in 30 seconds.")
                                        await asyncio.sleep(30)
                                        await thread.delete()
                                        break
                                    else:
                                        await thread.send(f"{player1.mention} has {player1_hp}HP left!")

                        # end of minigame loop
                        # delete the thread



                # send the first message

            else:
                await ctx.respond(f"{user.mention} has declined the challenge!")
            return


def setup(bot):
    bot.add_cog(minigame_commands(bot))
