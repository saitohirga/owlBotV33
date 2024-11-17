import discord
from discord import app_commands
from time import gmtime, strftime
import datetime
import data.key
import openai

MY_GUILD = discord.Object(id=458765854624972811)  # Replace with your guild ID

openai.api_key = data.key.openai_key

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

def format_time_difference(diff: datetime.timedelta) -> str:
    total_seconds = int(diff.total_seconds())
    years, remainder = divmod(total_seconds, 31536000)  # 1 year = 31536000 seconds
    months, remainder = divmod(remainder, 2592000)      # 1 month = 2592000 seconds
    days, remainder = divmod(remainder, 86400)         # 1 day = 86400 seconds
    hours, remainder = divmod(remainder, 3600)         # 1 hour = 3600 seconds
    minutes, seconds = divmod(remainder, 60)
    return f"{years} years, {months} months, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    
    # Set the bot's status to "Watching FAU Discord"
    activity = discord.Activity(type=discord.ActivityType.watching, name="FAU Discord, I see yall")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("Bot status set to 'Watching FAU Discord'")

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
        date2 = '2019-11-18 12:25:34'
        date1 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
        response = f"Hello {message.author.mention}, No rats spotted in the caf as of today. If this changes, DM Saito. Time since last seen: {format_time_difference(diff)}"
        await message.channel.send(response)

@client.tree.command()
async def rat(interaction: discord.Interaction):
    """Checks for that gosh darn rat!"""
    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    date2 = '2019-11-18 12:25:34'
    date1 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
    msg = f"Hello {interaction.user.mention}, No rats spotted in the caf as of today. If this changes, DM Saito. Time since last seen: {format_time_difference(diff)}"
    await interaction.response.defer(thinking=True)
    await interaction.followup.send(msg)

@client.tree.command()
async def bird(interaction: discord.Interaction):
    """Checks for birds"""
    datetimeFormat = '%Y-%m-%d %H:%M:%S'
    date2 = '2021-10-20 07:44:36'
    date1 = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    diff = datetime.datetime.strptime(date1, datetimeFormat) - datetime.datetime.strptime(date2, datetimeFormat)
    await interaction.response.send_message(
        f"Hello {interaction.user.mention}, No birds spotted in the caf as of today. If this changes, DM Saito. Time since last seen: {format_time_difference(diff)}"
    )

@client.tree.command()
@app_commands.rename(text_to_send='text')
@app_commands.describe(text_to_send='Reports on what our owl is thinking')
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

@client.tree.command()
@app_commands.default_permissions(manage_messages=True)
@app_commands.describe(question="The question you want to ask OpenAI")
async def ask_openai(interaction: discord.Interaction, question: str):
    """Ask OpenAI a question"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Named Owsley's Freind, you are a mascot of the College florida atlantic university."},
                {"role": "user", "content": question}
            ]
        )
        answer = response["choices"][0]["message"]["content"]
        await interaction.response.send_message(f"🤖 {answer}")
    except Exception as e:
        await interaction.response.send_message(f"⚠️ An error occurred: {str(e)}")   

client.run(data.key.token)