from typing import Optional

import discord
from discord import app_commands
from time import gmtime, strftime
import datetime
import data.key


MY_GUILD = discord.Object(id=458765854624972811)  # replace with your guild id


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    
    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.tree.command()
async def rat(interaction: discord.Interaction):
    """Checks for that gosh darn rat!"""
    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    date2 = '2019-11-18 12:25:34'
    date1 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
    await interaction.response.send_message(f"Hello {interaction.user.mention}, No rats spotted in the caf as of today, if this changes DM Saito, time since " f"last seen {diff}")   

@client.tree.command()
async def bird(interaction: discord.Interaction):
     """Checks for birds"""
     datetimeFormat = '%Y %m %d %H:%M:%S'
     date2 = '2021 10 20 7:44:36'
     date1 = strftime("%Y %m %d %H:%M:%S", gmtime())
     diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
     await interaction.response.send_message(f"Hello {interaction.user.mention}, No bird spotted in the caf as of today, if this changes DM Saito, time since last seen {diff}")

@client.tree.command()
@app_commands.rename(text_to_send='text')
@app_commands.describe(text_to_send='send')
@app_commands.default_permissions(manage_messages=True)
async def owl(interaction: discord.Interaction, text_to_send: str):
    """Sometimes sends a cute owl"""
    await interaction.response.send_message(text_to_send, hidden=True)

client.run(data.key.token)                                          