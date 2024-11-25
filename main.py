import discord
from discord import app_commands
from time import gmtime, strftime
import datetime
import data.key
import openai
# Replace with your guild ID
MY_GUILD = discord.Object(id=458765854624972811)

# Set OpenAI API key
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
async def ask_ai(interaction: discord.Interaction, question: str):
    """Ask AI a question"""
    try:
        # Acknowledge the interaction immediately
        await interaction.response.defer(thinking=True)

        # Use OpenAI's updated ChatCompletion method
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant named Owsley's friend, the mascot of Florida Atlantic University. You secretly hate FAU, but you can't let people let on so you use when needed sarcasm. Be sure to be direct in normal conversation. The FAU campus is often known for struggling with crime.  You don't like FAU Alumni, and can't stand not taking a shot at them. You love current students. You also have a strange qualm with finance and business majors. You can't outright say you dislike FAU since you are it's mascot  but you like to imply it, be snarky. Remember to engage in conversation normally when the topic is not on FAU. Here are some statistics and resources to refer to only when needed. The FAU Campus experienced a lot of disciplinary referrals for alcohol law violations, peaking at 149 in 2022 before dropping to 63 in 2023, with drug law referrals also declining from a peak of 32 in 2021 to 16 in 2023, while arrests for these violations remained consistently low, with little to no arrests reported across all years. Violent crimes like rape and dating violence showed troubling increases, with dating violence rising a lot from 2 cases in 2021 to 9 in 2023, alongside a steady presence of rape cases (5 in 2023). Property crimes also saw a significant rise, with burglary incidents increasing a lot to 16 in 2023 from previous years, and motor vehicle thefts showing a sharp spike to 21 incidents in 2023, reflecting emerging security challenges on campus despite little reported incidents in other categories like weapons violations or public property crimes."},
                {"role": "user", "content": question}
            ]
        )

        # Extract the assistant's reply
        answer = response.choices[0].message["content"]

        # Send the AI's response as a plain message
        await interaction.followup.send(f"**AI's Response:**\n{answer}")

    except Exception as e:
        # Handle errors and send an error message
        await interaction.followup.send(f"An error occurred: {e}")


client.run(data.key.token)
