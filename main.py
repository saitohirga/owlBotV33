from typing import Optional
import discord
from discord import app_commands
from time import gmtime, strftime
import datetime
import data.key
import asyncio

MY_GUILD = discord.Object(id=458765854624972811)  # Replace with your guild ID

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.rat_listener_enabled = True  # Initialize the rat listener toggle here

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
intents.messages = True  # Enable message intents
intents.message_content = True  # Enable message content intents
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.event
async def on_message(message: discord.Message):
    # Check if the listener is enabled
    if not client.rat_listener_enabled:
        return

    # Ignore bot's own messages
    if message.author.bot:
        return

      # Trigger only if `.rat` is at the start of the message
    if message.content.strip().startswith(".rat"):
     datetimeFormat = '%Y-%m-%d %H:%M:%S'
     date2 = '2021-10-20 07:44:36'
     date1 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
     diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
     response = f"Hello {message.author.mention}, No bird spotted in the caf as of today, if this changes DM Saito, time since last seen {diff}"
     await message.channel.send(response)

@client.tree.command()
async def rat(interaction: discord.Interaction):
    """Checks for that gosh darn rat!"""
    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    date2 = '2019-11-18 12:25:34'
    date1 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
    msg = f"Hello {interaction.user.mention}, No rats spotted in the caf as of today, if this changes DM Saito, time since last seen {diff}"
    await interaction.response.defer(thinking=True)
    await interaction.followup.send(msg)

@client.tree.command()
async def bird(interaction: discord.Interaction):
    """Checks for birds"""
    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    date2 = '2021-10-20 07:44:36'
    date1 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
    await interaction.response.send_message(f"Hello {interaction.user.mention}, No bird spotted in the caf as of today, if this changes DM Saito, time since last seen {diff}")

@client.tree.command()
@app_commands.rename(text_to_send='text')
@app_commands.describe(text_to_send='reports on what our owl is thinking')
@app_commands.default_permissions(manage_messages=True)
async def owlthought(interaction: discord.Interaction, text_to_send: str):
    """Reports what our owl is thinking"""
    await interaction.response.send_message(text_to_send)

@client.tree.command()
@app_commands.default_permissions(manage_messages=True)
async def toggle_listener(interaction: discord.Interaction):
    """Toggles the .rat and mention listener on or off."""
    client.rat_listener_enabled = not client.rat_listener_enabled
    status = "enabled" if client.rat_listener_enabled else "disabled"
    await interaction.response.send_message(f"The .rat listener has been {status}.")

client.run(data.key.token)
