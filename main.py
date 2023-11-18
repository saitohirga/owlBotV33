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
    await interaction.response.send_message(f"Hello  {interaction.user.mention}, No rats spotted in the caf as of today, if this changes DM Saito, time since " f"last seen {diff}")


    @discord.app_commands.command(description="Echoes the message to a specified channel")
    @discord.app_commands.describe(message="The message to echo")
    @discord.app_commands.describe(channel="The channel to send the message to")
    async def secret_echo(self, interaction: discord.Interaction, message: str, channel: discord.TextChannel):
        role_id = 882444308857384991  # Your specific role ID

        # Check if the user has the required role
        if discord.utils.get(interaction.user.roles, id=role_id):
            await channel.send(message)
            await interaction.response.send_message(f"Message sent to {channel.mention}", ephemeral=True)
        else:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)



   

client.run(data.key.token)                                          