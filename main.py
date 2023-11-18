from typing import Optional

import discord
from discord import app_commands
from time import gmtime, strftime
import datetime
import data.key
from discord.ext import commands

MY_GUILD = discord.Object(id=458765854624972811)  # replace with your guild id


class MyClient(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix="!", intents=intents)
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


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Correctly defining the slash command within the cog
    @discord.app_commands.command(name="secret_echo", description="Echoes the message to a specified channel")
    @discord.app_commands.describe(message="The message to echo")
    async def secret_echo(self, interaction: discord.Interaction, message: str):
        role_id = 882444308857384991  # Your specific role ID

        # Check if the user has the required role
        if discord.utils.get(interaction.user.roles, id=role_id):
            # Replace 'your_channel_id' with the ID of the channel you want the message to be sent to
            channel = self.bot.get_channel(458765855115968513)
            if channel:
                await channel.send(message)
                await interaction.response.send_message(f"Message sent to {channel.mention}", ephemeral=True)
            else:
                await interaction.response.send_message("Channel not found.", ephemeral=True)
        else:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)

# Add the cog to the bot
client.add_cog(MyCog(client))


   

client.run(data.key.token)                                          